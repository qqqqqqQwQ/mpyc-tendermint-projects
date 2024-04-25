from sklearn.tree import DecisionTreeClassifier
import pickle
import os
from datetime import datetime
import joblib

# 保存模型到文件

# 定义一个函数来解析文本决策树并转换为字典格式
def parse_tree(tree_text):
    tree_dict = {}
    current_condition = None
    for line in tree_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if 'if' in line:
            parts = line.split('==')
            feature = parts[0].split('if')[1].strip()
            value = parts[1].split(':')[0].strip()
            result = parts[1].split(':')[1].strip()
            current_condition = (feature, value)
            tree_dict[current_condition] = result
        else:
            parts = line.split(':')
            value = parts[0].strip()
            result = parts[1].strip()
            tree_dict[current_condition][value] = result
    print(tree_dict)
    return tree_dict
# 文本形式的决策树
# tree_text = """
# if Credit_History == :
# |   if Self_Employed == : N
# |   if Self_Employed == No:
# |   |   if ApplicantIncome == A: N
# |   |   if ApplicantIncome == B: N
# |   |   if ApplicantIncome == C: Y
# |   |   if ApplicantIncome == D: Y
# ...
# """


# 定义一个函数来根据解析的决策树字典生成特征和目标数据
def create_dataset(tree_dict, features):
    X = []
    y = []
    for feature_values, result in tree_dict.items():
        feature_vector = [1 if feature_values[0] == feature else 0 for feature in features]
        X.append(feature_vector)
        y.append(1 if result == 'Y' else 0)
    return X, y


# 保存模型到文件
def saveModel(tree_text,features):
    tree_dict = parse_tree(tree_text)
    print(tree_dict)
    # features = ['Credit_History', 'Self_Employed', 'ApplicantIncome', 'LoanAmount', 'CoapplicantIncome','Property_Area', 'Education', 'Dependents', 'Gender', 'Married']
    X, y = create_dataset(tree_dict, features)
    # 使用sklearn训练决策树模型
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X, y)
    current_directory = os.path.dirname(__file__)
    save_directory = os.path.join(current_directory,"..", 'models','model_pkls')
    # 如果目录不存在，则创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # 定义模型保存路径
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 构造文件名
    file_name = f'decision_tree_model_{current_time}.pkl'
    model_path = os.path.join(save_directory, file_name)
    # 保存模型到文件
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)


# 定义一个函数来解析文本决策树并转换为字典格式

# 定义一个函数来根据解析的决策树字典生成特征和目标数据
# 保存模型到文件
def saveModel2(tree_text, features):
    tree_dict = parse_tree(tree_text)
    print(tree_dict)
    X, y = create_dataset(tree_dict, features)
    # 使用sklearn训练决策树模型
    model = DecisionTreeClassifier(max_depth=10)
    model.fit(X, y)
    current_directory = os.getcwd()
    save_directory = os.path.join(current_directory, 'models', 'model_pkls')
    # 如果目录不存在，则创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # 定义模型保存路径
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 构造文件名
    file_name = f'decision_tree_model_{current_time}.pkl'
    model_path = os.path.join(save_directory, file_name)
    # 保存模型状态到文件
    joblib.dump(model, model_path)

if __name__ == '__main__':
    file_path = "../models/model_txts/loan_predication_tree_2024-04-24_13-01-26.txt"
    with open(file_path, 'r') as file:
        tree_text = file.read()
    decision_tree = parse_tree(tree_text)
    # 假设你有一个名为 dataset 的 DataFrame
    # 使用 validate_dataset 函数对数据集进行验证
    features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
                'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    dataset=create_dataset(decision_tree,features)
    print(dataset)