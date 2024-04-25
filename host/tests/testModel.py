
from host.utils import text2treeArray,dataClean
from host.utils import dataAnalyseBytxt
import pandas as pd

model_path = "../models/model_txts/loan_predication_tree_2024-04-25_20-10-37.txt"
data_path="../mpcData/loan_predication_check.csv"



with open(model_path, 'r') as file:
    tree_text = file.read()
decision_tree = text2treeArray.parse_tree(tree_text)
# 读取数据
data = pd.read_csv(data_path)
dataset = dataClean.process_excel_file(data)
# 使用 validate_dataset 函数对数据集进行验证
predictions = dataAnalyseBytxt.validate_dataset(dataset, decision_tree)
print(predictions)