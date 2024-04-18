from quart import Quart, request, jsonify,send_file,redirect,url_for,make_response
from quart_cors import cors
import time
from datetime import datetime, timedelta
from secrets import token_hex
from unanimous.utils import get_task_status
from unanimous import route as Unanimous
from mpcData import ComputeData
from utils import check_auth_token_validity
app = Quart(__name__)
cors(app)
# 假设这里有一个字典，用于存储用户的目标页面信息
user_target_pages = {}

host_path="localhost"

# 维护所有数据集合
# 1.hosts=[{ip:"6.6.6.6",ports:[{port:"11",status:0},{port:"12",status:0}],remain:30},{ip:"7.7.7.7",ports:[{},{}],remain:60}]
# 2.tasks=[{task_name:"unanimous",task_id:xxx,task_passwd:"000",party_num:3,presents:0,status:1,nodes:[{ip:"6.6.6.6",port:"33",client_key:"66",host_index:'0',index:"1"},{}]},{}]

# 前端页面，返回登录页面
@app.route('/',methods=['GET'])
async def dddd():
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))
@app.route('/login',methods=['GET'])
async def login():
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return await send_file('static/login.html')
    else:
        return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
async def index():
    auth_token = request.cookies.get('auth_token')
    print(auth_token)
    if not auth_token:
        return redirect(url_for('login', redirect='/index'))
    else:
        return await send_file('static/index.html')
@app.route('/unanimous', methods=['GET'])
async def unanimous():
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return redirect(url_for('login', redirect='/unanimous'))
    else:
        return await send_file('static/unanimous.html')
# @app.route('/unanimous/login', methods=['POST'])
# async def unanimous_login():
#     data=await request.get_json()
#     ret= await unanimous.login(data)
#     return jsonify(ret)



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


@app.route('/unanimous/prepare', methods=['POST'])
async def unanimous_prepare(): # {client_key,patry_num}-》{node:{ip,port,index,client_key}}
    data=await request.get_json()
    ret= await Unanimous.TaskCreate(data)
    return jsonify(ret)
@app.route('/unanimous/join', methods=['POST'])
async def unanimous_join(): # {task_id,client_key}-》{node:{ip,port,index,client_key}}
    data=await request.get_json()
    ret= await Unanimous.TaskJoin(data)
    return jsonify(ret)
@app.route('/unanimous/status', methods=['POST'])
async def unanimous_status():# {task_id,client_key}-》{status,message}
    data=await request.get_json()
    status=get_task_status(data["task_id"])
    while status!=2:  # 设置超时时间为30秒
        print("正等待task的status变成2")
        # return jsonify({"status": status,"message": "请等待其他参与方加入..."})
        time.sleep(1)  # 休眠1秒，减轻服务器压力
    return jsonify({"status": status,"message":"多方计算已准备就绪"})


@app.route('/ot', methods=['GET'])
def ot():
    return send_file('static/ot.html')
@app.route('/sort', methods=['GET'])
def sort():
    return send_file('static/sort.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)  # 在端口80上运行网关服务