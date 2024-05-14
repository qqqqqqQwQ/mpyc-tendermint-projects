import pickle
import os
from datetime import datetime

# 定义节点类
class TreeNode:
    def __init__(self, feature=None, children=None, result=None):
        self.feature = feature  # 分裂特征
        self.children = children  # 子节点
        self.result = result  # 叶节点的类别值或结果值

# 递归构建决策树
def build_tree(data):
    if not data:
        return None

    # 获取当前特征
    feature, _, _ = data[0]

    # 创建节点
    node = TreeNode(feature=feature)

    # 分割数据
    children = {}
    while data and data[0][0] == feature:
        _, value, result = data.pop(0)
        if result != "":  # 如果结果不是空字符串，则当前节点是叶子节点
            children[value] = TreeNode(result=result)
        else:  # 如果结果是空字符串，则当前节点是内部节点
            children[value] = build_tree(data)
    node.children = children
    return node

def saveModel(sample_data):
    root_node = build_tree(sample_data)
    # 保存决策树为 .pkl 文件
    current_directory = os.path.dirname(__file__)
    save_directory = os.path.join(current_directory, "..", 'models', 'model_pkls')
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
        pickle.dump(root_node, f)
