import pandas as pd

def process_file(file):
    # 获取文件扩展名
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension == 'csv':
        # 如果是 CSV 文件，使用 read_csv() 函数读取数据
        data = pd.read_csv(file)
    elif file_extension in ['xls', 'xlsx']:
        # 如果是 Excel 文件，使用 read_excel() 函数读取数据
        data = pd.read_excel(file)
    else:
        # 如果既不是 CSV 文件也不是 Excel 文件，抛出异常或者进行其他处理
        raise ValueError("Unsupported file format")
    return data