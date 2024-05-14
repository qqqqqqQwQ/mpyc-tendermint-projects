# import pickle
import joblib
from sklearn import tree
import graphviz
# 加载模型

# 模型路径
model_path = '../models/model_pkls/decision_tree_model_2024-04-25_16-15-23.pkl'


# 加载.pkl文件
clf = joblib.load(model_path)

# 可视化决策树
dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names=clf.feature_names,
                     class_names=clf.target_names,
                     filled=True, rounded=True,
                     special_characters=True)

graph = graphviz.Source(dot_data)
graph.render("decision_tree_visualization")