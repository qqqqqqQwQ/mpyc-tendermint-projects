import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier



# 示例函数调用

def getResult(data,path): # 传进来的就是pd的dataFrame类型
    # 假设已经加载了保存的模型到 loaded_model 变量中
    # 从文件中加载模型
    with open(path, 'rb') as f:
        loaded_model = pickle.load(f)
    # 假设你的CSV文件中的数据与模型训练时的特征顺序一致
    X = data.drop('Loan_Status', axis=1)  # 移除目标变量

    # 使用加载的模型进行预测
    predictions = loaded_model.predict(X)
    # 打印预测结果
    print("预测结果:", predictions)
    return predictions

if __name__ == "__main__":
    data=pd.read_csv("../mpcData/loan_predication_check.csv")
    path="../models/model_pkls/decision_tree_model_2024-04-23_21-51-32.pkl"
    predication=getResult(data,path)
    print(predication)