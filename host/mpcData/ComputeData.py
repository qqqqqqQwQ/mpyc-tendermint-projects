import requests
import random
import json
import os

# 获取最新的当前空闲的ip:port,现在用json假装redis数据库，读写都是整个json文件，
def get_data():
    # 获取当前文件的目录路径
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建相对路径
        relative_path = os.path.join(current_dir, 'data.json')
        with open(relative_path, 'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict
    except Exception:
        print('get mpc data error')
def save_data(load_dict):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(current_dir, 'data.json')
        with open(relative_path, 'w') as write_f:
            json.dump(load_dict, write_f, indent=4, ensure_ascii=False)
    except Exception as e:
        print('save data error:', e)




# 预定所需的m个nodes=[ip,port,index],并修改hosts的状态。失败返回0。（未修改tasks）
# 如果是先向node发送task，等成功以后再修改data中hosts和tasks的状态，可能会发生数据访问冲突？导致后面的参与方收到计算资源忙碌的情况？此处等task失败再undo
def get_task_nodes(m):
    try:
        data = get_data()
        # 这里应该按照data["host"]中remain状态选择m个selectde_hosts,如果remain不满足m需求，返回0
        spare_host = []
        print("请求计算节点数：", m)
        for host in data['hosts']:
            if host['remain'] > 0:
                spare_host.append(host)
        if len(spare_host) < m:
            raise ValueError("当前服务器计算繁忙，计算节点不足，请等待")
        selected_hosts = random.sample(spare_host, m)
        result = []
        index = 0
        for host in selected_hosts:
            ip = host["ip"]
            id = host["id"]
            for port_info in host["ports"]:
                if port_info["status"] == 0:
                    port = port_info["port"]
                    port_info["status"] = 1
                    host["remain"] -= 1
                    result.append({"ip": ip, "port": port, "index": index, "client_key": "","host_id":id})
                    index += 1
                    break  # 继续下一个IP的选择
        # 这个判断应该在一开始remain不够用时就返回，待修改
        save_data(data)
        return result
    except Exception as e:
        print(f"get_task_nodes error:{e}")
        raise Exception(e)

# 当预定的nodes遇到错误时，需要回退预定，释放hosts的资源
def undo_hosts(nodes,wrong_indexs):
    try:
        data = get_data()
        # 修改data.hosts
        for index, node in enumerate(nodes):
            host_index, port_index = find_node_index(node["ip"], node["port"])
            temp_ip=node["ip"],temp_port=node["port"]
            if (index in wrong_indexs):
                data["hosts"][host_index]["port"][port_index]["status"] = 2  # 更新为不可用
                print(f"{temp_ip}:{temp_port}不可用，已停用")
            else:
                data["hosts"][host_index]["port"][port_index]["status"] = 0  # 更新为可使用
                print(f"对于{temp_ip}:{temp_port}的预约已取消")
        save_data(data)
    except Exception as e:
        print(f"undo_host error:{e}")
# 添加计算任务
def tasks_add_task(task):
    try:
        data=get_data()
        data["tasks"].append(task)
        print("看看到底是不是这里tasks有问题：",data["tasks"])
        save_data(data)
        print("tasks_add_task成功")
        test=get_data()
        print("看看到底是不是这里tasks有问题：",test["tasks"])
    except Exception as e:
        print("tasks_add_task失败")
        raise ValueError("tasks_add_task失败")
# 当预定的tasks遇到错误时，需要回退预定，终止task
def tasks_remove_task(task):
    try:
        data = get_data()
        task_id = task["task_id"]
        index = find_task_index(task_id)
        _ = data["tasks"].pop(index)
        save_data(data)
    except Exception as e:
        print(f"tasks_remove_task error:{e}")
def undo_tasks(task):
    try:
        data = get_data()
        # 修改data.tasks
        nodes = task["nodes"]
        undo_hosts(nodes, [])
        tasks_remove_task(task)
        save_data(data)
    except Exception as e:
        print(f"undo_tasks error: {e}")
        raise Exception(e)


def get_server_port(id):
    try:
        data = get_data()
        hosts = data["hosts"]
        for host in hosts:
            if host["id"] == id:
                return host["server_port"]
        # return hosts[index]["port"]
    except Exception as e:
        print(f"get_server_port error:{e}")


def find_task_index(target_task_id):
    try:
        data = get_data()
        tasks = data["tasks"]
        print("当前的tasks状态：",tasks)
        print("接收到task_id:",target_task_id)
        for index, task in enumerate(tasks):
            print("遍历到当前的task_id:",task["task_id"])
            if task["task_id"] == target_task_id:
                return index
        return -1  # 如果没有找到对应的任务，则返回-1
    except Exception as e:
        print(f"find_task_index error:{e}")


def find_host_index(id):
    try:
        data = get_data()
        hosts = data["hosts"]
        for index, node in enumerate(hosts):
            if node.get("id") == id:
                return index
        return -1  # 如果没有找到对应的任何host，则返回-1
    except Exception as e:
        print(f"find_host_index error:{e}")

def find_node_index(ip,port):
    try:
        data = get_data()
        hosts = data["hosts"]
        for host_index, host in enumerate(hosts):
            if host.get("ip") == ip:
                for port_index, _port in enumerate(hosts[host_index]["ports"]):
                    if _port["port"] == port:
                        return host_index, port_index
        return -1  # 如果没有找到对应的node，则返回-1
    except Exception as e:
        print(f"find_node_index error:{e}")



# 将client_key加入到tasks的task中，若task人已满，status=2 (待解决，相同的client_key加入拒绝否
def task_addClient(task_id,client_key):
    try:
        print(f"正在将用户{client_key}添加到任务{task_id}中")
        # 1.将client_key添加进tasks
        index = find_task_index(task_id)
        if (index == -1):
            raise ValueError("task_id不合法")
        data = get_data()
        task_index = data["tasks"][index]["presents"]
        if (task_index >= data["tasks"][index]["party_num"]):
            raise ValueError("加入失败，当前参与方已满")
        data["tasks"][index]["nodes"][task_index]["client_key"] = client_key
        data["tasks"][index]["presents"] += 1
        if (data["tasks"][index]["presents"] == data["tasks"][index]["party_num"]):
            data["tasks"][index]["status"] = 2
        save_data(data)
        # 2.将node数据发送给对应的client，同时将client和task_id告诉node，但注意此时port应改为serverip而不是task_ip
        node1 = data["tasks"][index]["nodes"][task_index]
        node1["port"] = get_server_port(node1["host_id"])
        node1["task_id"] = task_id
        node1["party_num"] = data["tasks"][index]["party_num"]
        print("正在向client返回对接的node：", node1)
        return node1
    except Exception as e:
        print(f"task_addClient error:{e}")
        raise Exception(e)

def check_task_status(task_id):
    try:
        index = find_task_index(task_id)
        if (index == -1):
            raise ValueError("task_id不合法")
        data = get_data()
        return data["tasks"][index]["presents"] == data["tasks"][index]["party_num"]
    except Exception as e:
        print(f"task_addClient error:{e}")



def get_task_status(task_id):
    try:
        index = find_task_index(task_id)
        if (index == -1):
            raise ValueError("task_id不合法")
        data = get_data()
        return data["tasks"][index]["status"]
    except Exception as e:
        print(f"task_addClient error:{e}")


def task_removeClient(task_id,client_key):
    try:
        index = find_task_index(task_id)
        if (index == -1):
            raise ValueError("task_id不合法")
        data = get_data()
        nodes = data["tasks"][index]["nodes"]
        node_index = get_indexby_clientkey(nodes, client_key)
        data["tasks"][index]["nodes"][node_index]["client_key"] = ""
    except Exception as e:
        print(f"task_removeClient error:{e}")


def get_indexby_clientkey(nodes,client_key):
    try:
        data = get_data()
        tasks = data["tasks"]
        for index, node in enumerate(nodes):
            if node.get("client_key") == client_key:
                return index
        return -1  # 如果没有找到对应的node，则返回-1
    except Exception as e:
        print(f"task_removeClient error:{e}")


def checkClientKey(dddd):
    try:
        data = get_data()
        print(dddd)
        client_key = dddd["client_key"]
        for index,client in enumerate(data["clients"]):
            if client["client_key"] == client_key:
                name=data["clients"][index]["name"]
                return 1,name
        return 0,''
    except Exception as e:
        print("注意，前端有client_key为null的data通过")
        return 0,''

