import os
from datetime import datetime

def save_txt_file(content):
    # 获取当前时间
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 构造文件名
    file_name = f'loan_predication_tree_{current_time}.txt'

    # 获取当前文件目录
    # current_directory = os.path.dirname(__file__)
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 确定保存的目录
    save_directory = os.path.join(current_directory, 'models', 'model_txts')

    # 如果目录不存在，则创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # 构造文件路径
    file_path = os.path.join(save_directory, file_name)

    # 保存字符串内容到文本文件
    with open(file_path, 'w') as f:
        f.write(content)

    return file_path