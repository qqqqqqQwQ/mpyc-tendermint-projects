from sklearn.tree import DecisionTreeClassifier
import pickle
import os
from datetime import datetime

# 保存模型到文件

# 定义一个函数来解析文本决策树并转换为字典格式
def parse_tree(tree_text):
    lines = tree_text.split('\n')
    tree_dict = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if 'if' in line:
            condition, result = line.split(':')
            feature, value = condition.split('==')
            feature = feature.strip()
            value = value.strip()
            result = result.strip()
            tree_dict[(feature, value)] = result
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
    # features = ['Credit_History', 'Self_Employed', 'ApplicantIncome', 'LoanAmount', 'CoapplicantIncome','Property_Area', 'Education', 'Dependents', 'Gender', 'Married']
    X, y = create_dataset(tree_dict, features)
    # 使用sklearn训练决策树模型
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X, y)
    current_directory = os.getcwd()
    save_directory = os.path.join(current_directory, 'models','model_pkls')
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
