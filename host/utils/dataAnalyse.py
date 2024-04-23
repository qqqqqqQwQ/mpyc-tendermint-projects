import pickle
import pandas as pd


def getResult(data): # 传进来的就是pd的dataFrame类型
    # 假设已经加载了保存的模型到 loaded_model 变量中
    # 从文件中加载模型
    with open('decision_tree_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    # 假设你的CSV文件中的数据与模型训练时的特征顺序一致
    X = data.drop('Loan_Status', axis=1)  # 移除目标变量
    X = pd.get_dummies(X)  # 对分类变量进行独热编码

    # 使用加载的模型进行预测
    predictions = loaded_model.predict(X)

    # 打印预测结果
    print("预测结果:", predictions)
    return predictions

