from quart import Quart, request, jsonify,send_file
from quart_cors import cors
from node_utils import task_prepare,check_client,compute_task,after_compute,task_undo_prepare
import platform
import threading
import time
import os
import subprocess

from mpyc.runtime import mpc
import argparse
import asyncio
import sys

app =Quart(__name__)
cors(app)

server_port=33331


@app.route('/prepare', methods=['POST'])
async def prepare(): # {task}->{}
    data =await request.get_json()
    try:
        task_prepare(data)
        return jsonify({'code': 200, 'message': 'Task prepared successfully'})
    except ValueError as e:
        print(e)  # 打印错误信息
        return jsonify({'code': 500, 'message': str(e)})

@app.route('/undo_prepare', methods=['POST'])
async def undo_prepare(): # {task}->{}
    data =await request.get_json()
    try:
        task_undo_prepare(data)
        print("正在撤销任务")
        return jsonify({'code': 200, 'message': 'Task undo_prepared successfully'})
    except ValueError as e:
        print(e)  # 打印错误信息
        return jsonify({'code': 500, 'message': str(e)})

@app.route('/unanimous/compute', methods=['POST'])
async def test(): # {vote,key,task_id}->{200,data}
    data =await request.get_json()  # 获取POST请求中的JSON数据
    print("接收到前端的数据，",data)
    try:
        # 0.验证输入，包括用户身份，避免同时参与多个计算
        check_client(data)
        # 1.找到task路径,验证任务合法性
        abc=compute_task(data)
        url=os.path.join(abc, "unanimous.py")
        task_id=data['task_id']
        #用task_id找到party_num,目前不实现node中存数据，所以party_num先由客户端提供
        # task=get_task_by_id(task_id)
        party_num=str(data['party_num'])

        index=str(data['index'])
        party_vote=str(data['party_vote'])
        current_os = platform.system()
        folder_path=task_id
        python_command = f"python {url} -M{party_num} -I{index} {party_vote} -C party{party_num}_{index}.ini"

        if current_os == "Windows":
            command = f"cd /d {folder_path} && {python_command}"
        else:
            command = f"cd {folder_path} && {python_command}"
        print("这是计算命令：",command)
        # 2.计算
        ret = subprocess.run(command,stdout=subprocess.PIPE, shell=True)
        # output = ret.stdout.decode()
        output = ret.stdout.decode('utf-8','ignore')
        print("计算结果：",output)
        # 3.先清除任务
        after_compute(task_id)
        return jsonify({'code': 200, 'data': output})
    except ValueError as e:
        print(e)  # 打印错误信息
        return jsonify({'code':500, 'message':str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)  # 在端口80上运行网关服务