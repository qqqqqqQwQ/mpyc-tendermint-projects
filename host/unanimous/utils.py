import json
import uuid
import aiohttp
from mpcData.ComputeData import get_task_nodes,task_addClient,task_removeClient,tasks_add_task, get_server_port,undo_hosts,undo_tasks

# 计算发起者创建计算任务，将自己的key添加进task中，客户和node端都获得task信息从而用于建立连接
async def create_task(data,task_name):
    try:
        # 1.解析data数据
        party_num = data['party_num']
        party_num = convert_to_integer(party_num)

        # 2.获取nodes,包括修改hosts状态，nodes中所有host准备好port
        spare_nodes=await get_spare_nodes(party_num)

        # 3.生成task，包括修改tasks状态，nodes中所有host:port准备好task
        task=await get_task(spare_nodes,task_name,party_num)

        # 4.成功创建task，返回
        return task
    except Exception as e:
        print(f"create_task error:{e}")  # 打印错误信息
        raise Exception(e)

async def get_spare_nodes(party_num):
    try:
        while 1:
            num = 1  # 3次配置失败后放弃
            # 2.1 先获取有哪些空闲node，从mpcdata获取[{"ip": ip, "port": port,"index":index,"client_key":""},{}]
            spare_nodes = get_task_nodes(party_num)
            # 2.2 从节点集中获取nodes，与nodes达成共识后返回可以计算的nodes=[{ip,port,index,key=""},{}]，
            nodes_is_ok, wrong_nodes_indexs = await talk_to_nodes(spare_nodes)  # 返回协商结果，若失败，返回失败的nodes
            if not nodes_is_ok:
                undo_hosts(spare_nodes, wrong_nodes_indexs)
                print(f"向计算节点借port失败,第{num}次")
                if num >= 3:
                    raise ValueError("计算节点繁忙，请等待")
                num += 1
                continue
            break
        return spare_nodes
    except Exception as e:
        raise Exception(e)
async def get_task(spare_nodes,task_name,party_num):
    try:
        task_id = str(uuid.uuid4())
        task_passwd = ""  # 密码先不搞，用来限制进入房间的，限制计算的是客户的key
        task_status = 1  # 尚无意义
        task = {"task_name": task_name, "task_id": task_id, "task_passwd": task_passwd, "party_num": party_num,
                "presents": 0, "status": task_status, "nodes": spare_nodes}

        # task插入tasks
        tasks_add_task(task)
        # 将task告诉nodes，包括任何一个node失败时撤销task分发
        task_is_ok = await send_task(task)
        print(f"task_isok:{task_is_ok}")
        # 失败则还原tasks数据，包括释放task涉及的host:post的资源(undo_hosts)
        if not task_is_ok:
            print("???")
            undo_tasks(task)
            raise ValueError("计算节点繁忙，请等待")
        return task
    except Exception as e:
        print(f"get_task error:{e}")
        raise Exception(e)

# data中应该实时跟踪hosts的port情况，默认data中数据合法，这个函数或许没必要
async def talk_to_nodes(spare_nodes):
    try:
        return 1,[]
        # 与nodes协商，ip:port是否空闲
        results=[]
        # results=send_node(spare_nodes) # [{status:200,data:""},{status:500,data:""}]
    except Exception as e:
        print(e)  # 打印错误信息
        return 0



# 获取task并分发给其中的ip:port，每一个创建文件夹task_"port"，创建.config，创建3个py文件
# 执行generate-certificates.py和generate-config-files.py
# task={task_name:xxx,id:xxx,passwd:xxx,nodes:[{id:,ip:,port:,party_key:},{}],party_num:3}

async def send_task(task):
    # http请求将task发给所有ip，返回添加成功
    send_node_list=[]
    try:
        for index,node in enumerate(task["nodes"]):
            port=get_server_port(node["host_id"])
            print("准备task中，拿到了"+node["ip"]+"的服务端口：",port)
            str=node["ip"]+":"+port
            await send_task_prepare(str,task) # 失败会走except的
            send_node_list.append(node)
        return 1
    except Exception as e:
        # print(f"Error sending task to {node['ip']}: {e}")
        for node in send_node_list:
            port = get_server_port(node["host_id"])
            str = node["ip"] + ":" + port
            try:
                print(f"正在取消{str}的计算任务")
                await undo_send_task_prepare(str, task)
            except Exception as e:
                print(f"给{str}撤销task时失败,错误：",e)
        return 0
async def undo_send_task_prepare(ip_port,task):
    url = f"http://{ip_port}/undo_prepare"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=task) as response:
                if response.status == 200:
                    print(f"Task_undo sent successfully to {ip_port}")
                    return 1
                else:
                    print(f"Failed to send task_undo to {ip_port}. Status code: {response.status}")
                    raise ValueError(
                        f"task_undo发送给{ip_port}时，错误: {response.status}-{getattr(response, 'message', '')}")
    except aiohttp.ClientError as e:
        print(f"Error sending task_undo to {ip_port}: {e}")
        raise e

async def send_task_prepare(ip_port, task_data):
    url = f"http://{ip_port}/prepare"  # 替换成实际的端点URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=task_data) as response:
                if response.status == 200:
                    print(f"Task sent successfully to {ip_port}")
                    return 1
                else:
                    print(f"Failed to send task to {ip_port}. Status code: {response.status}")
                    raise ValueError(f"task发送给{ip_port}时，错误: {response.status}-{getattr(response, 'message', '')}")
    except aiohttp.ClientError as e:
        print(f"发生错误：Error sending task to {ip_port}: {e}")
        raise e




# client告知node，node:{ip,port,}
async def add_client_to_task(task_id,client_key):
    try:
        node=task_addClient(task_id,client_key)
        port = get_server_port(node["host_id"])
        print("准备client中，拿到了" + node["ip"] + "的服务端口：", port)
        str = node["ip"] + ":" + port
        # client_is_ok=await send_node_client(str,task_id,client_key)
        client_is_ok=1
        print(f"是否已成功向{str}部署client：",client_is_ok)
        if client_is_ok:
            return node
        else:
            task_removeClient(task_id,client_key)
            raise ValueError("与计算节点连接失败")
    except Exception as e:
        print(e)  # 打印错误信息
        raise ValueError(f"add_client_to_task error:{e}")

async def send_node_client(ip, task_id, client_key):
    url = f"http://{ip}/prepare/link_to_Client"
    data = {
        "task_id": task_id,
        "client_key": client_key
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    print(f"Client key sent successfully to {ip} for task {task_id}")
                    return 1
                else:
                    print(f"Failed to send client key to {ip} for task {task_id}. Status code: {response.status}")
                    return 0
    except aiohttp.ClientError as e:
        print(f"Error sending client key to {ip} for task {task_id}: {e}")
        raise e


def convert_to_integer(value):
    try:
        # 尝试将参数转换为整数类型
        return int(value)
    except Exception:
        # 如果转换失败，则返回默认值或者进行其他处理
        return None  # 或者抛出异常或者返回一个特定的错误值

def check_task_prepare(data):
    if(data["client_key"]==""):
        raise ValueError("client_key is empty")
    if(data["party_num"]==""):
        raise ValueError("party_num is empty")
    if(data["party_num"].isdigit()):
        return 0
    else:
        raise ValueError("party_num is not a number")

def check_task_join(data):
    if(data["client_key"]==""):
        raise ValueError("client_key is empty")
    if(data["task_id"]==""):
        raise ValueError("task_id is empty")


def get_task_status():
    return None

