from unanimous import utils


async def login(data):
    try:
        # check_client(data)
        return {"data":1,"code":200,"message":"登录成功"}
    except Exception as e:
        print(e)  # 打印错误信息
        return {'code': 401, 'message': "身份有误，登录失败"}

async def TaskCreate(data):
    # 第一个用户创建计算任务，等待所有其他参与者加入
    try:
        # 0.判断输入的合法性
        utils.check_task_prepare(data)

        # 1.根据用户post,创建计算任务，获取计算节点，修改节点数据状态
        # 2.所有node接取task任务，task->tasks[]
        task =await utils.create_task(data, "unanimous")
        print(f"计算任务已部署,现向客户返回task_id：",task)

        # 原来想着创建任务以后就将用户加入任务，发现很多无法回滚的bug，所以统一在前端再发起加入请求
        # 3.为当前用户分配task中的ip:post,修改task，并告知用户；告知node，用户key
        # node = await utils.add_client_to_task(task["task_id"], data["client_key"])  # 同时修改tasks，告知用户和node
        # node={ip,port,task_id,client_key,party_num}
        return {'code': 200, 'data': "计算任务已部署，请加入："+task['task_id']}
    except Exception as e:
        print(f"TaskCreate error:{e}")  # 打印错误信息
        return {'code': 500, 'message': str(e)}

async def TaskJoin(data):
    # 为当前用户分配task中的ip:post,修改task，并告知用户；告知node，用户key
    # add_client_to_task(task，key) #修改tasks，告知用户和node
    try:
        # 0.验证输入合法性
        utils.check_task_join(data)
        node = await utils.add_client_to_task(data["task_id"], data["client_key"])
        return {'code': 200, 'data': node}
    except Exception as e:
        print(e)  # 打印错误信息
        return {'code': 500, 'message': str(e)}