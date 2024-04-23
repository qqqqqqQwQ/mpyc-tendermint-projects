
from quart import Quart, request, jsonify,send_file,redirect,url_for,make_response
from quart_cors import cors
from datetime import datetime, timedelta
from secrets import token_hex
from unanimous.utils import get_task_status
from unanimous import route as Unanimous
from mpcData import ComputeData
from utils import dataClean,file2pd,text2model
import platform
import os
import subprocess
import pandas as pd
app = Quart(__name__)
cors(app)
# 假设这里有一个字典，用于存储用户的目标页面信息
user_target_pages = {}

host_path="localhost"

# 前端页面，返回登录页面
@app.route('/',methods=['GET'])
async def dddd():
    # auth_token = request.cookies.get('auth_token')
    # if not auth_token:
    #     return redirect(url_for('login'))
    # else:
    return redirect(url_for('id3gini'))
@app.route('/login',methods=['GET'])
async def login():
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return await send_file('static/login.html')
    else:
        return redirect(url_for('id3gini'))

@app.route('/id3gini', methods=['GET'])
async def id3gini():
    auth_token = request.cookies.get('auth_token')
    # if not auth_token:
    #     return redirect(url_for('login', redirect='/id3gini'))
    # else:
    return await send_file('static/id3gini.html')
# 登录接口
@app.route('/login', methods=['POST'])
async def login_post():
    # 假设这里是验证用户登录的逻辑
    data = await request.get_json()
    client_key = data.get('client_key')
    redirect_url = data.get('redirect_url')
    client_is_exist, client_name = ComputeData.checkClientKey(data)
    print("client_is_exist:",client_is_exist)
    if client_is_exist==1:
        # 处理用户登录逻辑，验证用户名密码等
        # 假设验证成功，设置认证cookie等操作
        auth_token = token_hex(16)  # 生成随机的复杂字符串作为 auth_token
        expire_time = datetime.now() + timedelta(hours=1)  # 设置过期时间为 1 小时后

        # 创建响应对象
        response =await make_response(jsonify({'auth_token': auth_token}))

        # 设置认证cookie
        response.set_cookie('auth_token', auth_token)
        response.set_cookie('client_key', client_key)
        response.headers['Access-Control-Allow-Origin'] = host_path
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        # 如果客户端密钥无效，则返回 401 Unauthorized 错误
        return jsonify({'error': 'Invalid client key'}),401
@app.route('/logout', methods=['POST'])
async def logout():
    # 创建响应对象
    response = jsonify({'message': 'Logout successful'})

    # 将认证cookie的过期时间设置为过去的时间点，以删除cookie
    expire_time = datetime.now() - timedelta(days=1)
    response.set_cookie('auth_token', '', expires=expire_time)
    response.set_cookie('client_key', '', expires=expire_time)

    # 设置允许跨域请求的头部信息
    response.headers['Access-Control-Allow-Origin'] = host_path
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

@app.route('/id3gini/compute', methods=['POST'])
async def test():
    try:
        file_path = os.path.join(os.getcwd(), 'id3gini', 'data', 'id3', 'loan_predication.csv')
        file = (await request.files)['file']
        print("接收到前端的数据，", file)
        data = file2pd.process_file(file)
        # data = pd.DataFrame(data)
        # 将数据处理好后放进文件夹中可以直接被id3gini调用
        dataClean.process_excel_file(data).to_csv(file_path, index=False)

        # 以下是多方计算
        folder_path='id3gini'
        current_os = platform.system()
        # url=os.path.join(".py")
        task_num=7
        # python_command = f"python {folder_path} -M{party_num} -I{index} {party_vote} -C party{party_num}_{index}.ini"
        python_command = f"python id3gini.py -i {task_num}"

        if current_os == "Windows":
            command = f"cd /d {folder_path} && {python_command}"
        else:
            command = f"cd {folder_path} && {python_command}"
        print("这是计算命令：",command)
        # 2.计算
        ret = subprocess.run(command,stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        # output = ret.stdout.decode()
        output = ret.stdout.splitlines()
        outputInLines = []
        sign = False
        for s in output:
            if not sign:
                if s == 'TreeOutPutStartBelow':
                    sign = True
            else:
                outputInLines.append(s)
        outputInLines.pop() # 弹出第一行空格
        output = '\n'.join(outputInLines)
        print("计算结果：", output)

        # 尝试将结果变成决策树模型
        text2model.saveModel(output)
        return jsonify({'code': 200, 'data': output})
    except Exception as e:
        print(e)  # 打印错误信息
        return jsonify({'code':500, 'message':str(e)})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)  # 在端口8088上运行服务