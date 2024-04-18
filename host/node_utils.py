
import os
import shutil
import subprocess
import platform
# 指定要创建的文件夹路径
# folder_path = "/path/to/new/folder"

# 使用 os.makedirs() 创建文件夹

def task_prepare(task):
    try:
        task_name = task["task_name"]
        file_name = task["task_id"]
        party_num = task["party_num"]
        nodes = task["nodes"]
        folder_path = get_config_path(file_name)
        task_path = get_task_path(file_name)
        current_directory = os.getcwd()
        # 1.创建文件夹
        os.makedirs(folder_path)
        print("文件夹创建成功！")
        # 2.将文件放入对应的位置准备执行
        # 源文件路径
        source_file1 = os.path.join(current_directory, "demos",".config", "generate-config-files.py")
        source_file2 = os.path.join(current_directory, "demos",".config" ,"generate-certificates.py")
        source_file3 = os.path.join(current_directory, "demos",task_name+".py")
        # 目标文件路径
        destination_file1 = os.path.join(folder_path, "generate-config-files.py")
        destination_file2 = os.path.join(folder_path, "generate-certificates.py")
        destination_file3 = os.path.join(task_path, task_name+".py")
        shutil.copy(source_file1, destination_file1)
        shutil.copy(source_file2, destination_file2)
        shutil.copy(source_file3,destination_file3)
        print("文件复制成功！")
        # 3.运行两个g.py
        current_os = platform.system()
        common_command = f"cd {folder_path} && python"
        if current_os == "Windows":
            command1 = f"{common_command} {destination_file1} -m {party_num}"
            command2 = f"{common_command} {destination_file2}"
        elif current_os == "Linux":
            command1 = f"{common_command} {destination_file1} -m {party_num}"
            command2 = f"{common_command} {destination_file2}"
        else:
            print("Unsupported operating system")
            exit()
        # str1="cd "+folder_path+" ; python"+" "+destination_file1 +" "+"-m"+" "+ str(party_num)
        # str2="cd "+folder_path+" ; python"+" "+destination_file2
        for i in range(party_num):
            # str1+=" "+nodes[i]["ip"]+":"+nodes[i]["port"]
            command1+=" "+nodes[i]["ip"]+":"+nodes[i]["port"]
            print("配置parties的ip:port，command:",command1)
        ret=subprocess.run(command1,stdout=subprocess.PIPE,shell=True)
        ret=subprocess.run(command2,stdout=subprocess.PIPE,shell=True)
        return 1
    except OSError as e:
        # 如果文件夹已经存在，会抛出 OSError 错误
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"文件夹{folder_path}已删除")
        raise ValueError(f"任务部署失败：{e}")

def task_undo_prepare(task):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # 删除同级的名为“abc”的文件夹
        task_dir = os.path.join(current_dir, task["task_id"])
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
            print(f"Deleted {task_dir}")
        else:
            print(f"{task_dir} does not exist")
            raise ValueError(f"{task_dir} does not exist")
    except Exception as e:
        raise ValueError("error:",e)
def check_client(data):
    if(data["client_key"]==""):
        raise ValueError("client_key is empty")
    if(data["task_id"]==""):
        raise ValueError("task_id is empty")
    if(data["party_vote"]==""):
        raise ValueError("party_vote is empty")
    if(data["index"]==""):
        raise ValueError("index is empty")

def compute_task(data):
    # 寻找任务位置
    folder_name=data["task_id"]
    current_directory = os.getcwd()
    # 拼接文件夹路径
    folder_path = os.path.join(current_directory, folder_name)
    # 检查文件夹是否存在
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"找到 '{folder_name}' 任务")
        return folder_path
    else:
        raise ValueError(f"计算任务 '{folder_name}' 不存在")
    # 验证client_key，这一步先不做

def get_task_by_id(task_id):
    return 0

def after_compute(task_id):
    # 1.先将结果保存到区块链
    # 2.清除任务
    current_directory = os.getcwd()
    # 拼接文件夹路径
    folder_path = os.path.join(current_directory, task_id)
    try:
        # 递归删除文件夹
        shutil.rmtree(folder_path)
        print(f"文件夹 '{folder_path}' 已成功删除。")
    except Exception as e:
        print(f"销毁计算任务 '{folder_path}' 时出错：{e}")
        raise ValueError(e)

def get_config_path(task_id):
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 指定相对路径
    relative_path = task_id
    config_path=".config"
    # 使用 os.path.join() 将当前目录和相对路径拼接起来
    folder_path = os.path.join(current_directory, relative_path,config_path)
    return folder_path

def get_task_path(task_id):
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 指定相对路径
    relative_path = task_id
    # 使用 os.path.join() 将当前目录和相对路径拼接起来
    task_path = os.path.join(current_directory, relative_path)
    return task_path