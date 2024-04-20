"""
kvstore demo
"""

import subprocess
import requests
import json
import base64
import os
import socket

# 本地测试
tendermint_port = 26657
ip = 'localhost'


def check_port(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(3)
    ret = 0
    try:
        sk.connect((ip, tendermint_port))
        print("server port connect OK! ")
    except Exception:
        print("server port not connect!")
        ret = 1
    sk.close()
    return ret


def rpc(cmd):
    rp = requests.get(cmd).json()
    return rp


if check_port('localhost', 26657) != 0:
    print('tendermint is not running')
    exit(1)
    # 下面本来想处理tendermint未启动的情况
    # 但是使用subprocess启动tendermint后会直接跳转到区块滚动页面, 暂时无法解决, 故暂且搁置
    '''
    if os.system('lsof -i :26657') == 0:
        print('当前端口正被占用, 终止占用端口进程')
        ret = subprocess.Popen('lsof -i :26657',shell=True,stdout=subprocess.PIPE)
        out = str(ret.stdout.read(),'utf-8')
        print('out: ',out)
        loc = out.find(':')
        loc_s, loc_e = loc+1, loc+6
        target_pid = int(out[loc_s:loc_e])
        print('kill -9 ' + str(target_pid))
        if not os.system('kill -9 ' + str(target_pid)):
            print('成功结束进程, 即将启动tendermint')
        else:
            print('结束失败, 退出程序')
            exit(1)
    # 在子进程中运行 tendermint 和 abci
    print('在子进程中运行tendermint')
    tendermint_process = subprocess.run(
        'tendermint init;tendermint node --proxy_app=kvstore'
        ,shell=True)
    '''


while 1:
    print("""
    *Kvstore test 0.1*
    Menu:
    a): input a kv pair
    b): query for a value
    c): exit
    """)
    choice = input("Please input your choice: ")
    if choice == 'a':
        key = input("key:")
        value = input("value:")
        command = ('http://localhost:26657/broadcast_tx_commit?tx=' +
                   '"' + key + '=' + value + '"')
        response = rpc(command)
        if 'error' in response:
            print("key already exists")
        else:
            print("Adding successfully:")
            print('hash: ',response['result']['hash'],
                  '\nheight location: ', response['result']['height'])
        input('press any key to continue...')
    elif choice == 'b':
        key = input("please input the key: ")
        command = 'http://localhost:26657/abci_query?data="' + key + '"'
        response = rpc(command)
        if response['result']['response']['log'] == 'exists':
            print('key exist, value:', end=' ')
            print(str(base64.b64decode(response['result']['response']['value'])
                      , 'utf-8'))
        else:
            print('key does not exist')
        input('press any key to continue...')
    elif choice == 'c':
        print("Thanks for your using")
        exit(0)
    else:
        print("wrong input, please try again")
        choice = ''
        input('press any key to continue...')
