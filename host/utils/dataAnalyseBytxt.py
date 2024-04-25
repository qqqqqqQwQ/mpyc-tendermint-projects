import pandas as pd
from host.utils import dataClean,text2treeArray

def parse_decision_tree(tree_text):
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
# def parse_decision_tree(tree_text):

def predict_sample(sample, decision_tree):
    try:
        print(1111)
        current_feature = decision_tree[0][0]
        print(current_feature)
        for index, row in enumerate(decision_tree):
            print(index)
            print(row)
            print(current_feature)
            feature = row[0]
            if not current_feature == feature:
                continue
            value = row[1]
            result = row[2]
            print(3333)
            print(result)
            print(feature)
            print(value,type(value))
            print(sample[feature],type(sample[feature]))
            print(4444)
            current_feature = feature
            if sample[feature] == value:
                print("匹配成功")
                if result == '':
                    print(index)
                    current_feature = decision_tree[index + 1][0]
                    print(current_feature)
                    continue
                else:
                    print("出结果了：", result)
                    return result
            else:
                continue
    except Exception as e:
        print(e)




def validate_dataset(dataset, decision_tree):
    predictions = []
    print(dataset)
    for index, row in dataset.iterrows():
        print(9999)
        print(row)
        prediction = predict_sample(row, decision_tree)
        predictions.append(prediction)
    return predictions

if __name__ == "__main__":
    # 读取树
    file_path="../models/model_txts/loan_predication_tree_2024-04-25_20-10-37.txt"
    with open(file_path, 'r') as file:
        tree_text = file.read()
    decision_tree =text2treeArray.parse_tree(tree_text)
    # 读取数据
    data=pd.read_csv("../mpcData/loan_predication_check.csv")
    dataset=dataClean.process_excel_file(data)
    # 使用 validate_dataset 函数对数据集进行验证
    predictions = validate_dataset(dataset, decision_tree)
    print(predictions)