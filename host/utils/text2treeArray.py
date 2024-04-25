def parse_tree(tree_text):
    tree_dict = []
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
            current_condition = (feature, value, result)
            tree_dict.append(current_condition)
        else:
            print("文本生成决策数组：传入的决策树某行缺失if字符")
    print(tree_dict)
    return tree_dict