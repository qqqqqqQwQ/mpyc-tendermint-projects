
from utils import text2treeArray,dataClean
from utils.dataAnalyseBytxt import validate_dataset
import pandas as pd

model_path = "models/model_txts/loan_predication_tree_2024-04-26_15-18-34.txt"
data_path= "mpcData/loan_predication_check.csv"



with open(model_path, 'r') as file:
    tree_text = file.read()
decision_tree = text2treeArray.parse_tree(tree_text)
# 读取数据
data = pd.read_csv(data_path)
dataset = dataClean.process_excel_file(data)
# 使用 validate_dataset 函数对数据集进行验证
loan_status_result = dataset['Loan_Status'].values
print(loan_status_result)
predictions = validate_dataset(dataset, decision_tree)
print(predictions)

# 初始化准确度计数器
accuracy_count = 0

# 比较两个数组对应位置的值
for i in range(len(loan_status_result)):
    if loan_status_result[i] == predictions[i]:
        accuracy_count += 1

# 计算准确度
accuracy = accuracy_count / len(loan_status_result) * 100
print("模型训练结果的准确度为: {:.2f}%".format(accuracy))