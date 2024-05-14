from utils import file2pd,dataClean,text2model,modeltxtRecord
import os
import platform
import subprocess
import pandas as pd

current_directory = os.path.dirname(__file__)
csv_path = os.path.join(current_directory,"mpcData","loan_predication_test.csv")
data = pd.read_csv(csv_path)
file_path = os.path.join(current_directory, 'id3gini', 'data', 'id3', 'loan_predication.csv')
dataClean.process_excel_file(data).to_csv(file_path, index=False)

# 训练模型
# 以下是多方计算
folder_path=os.path.join(current_directory,'id3gini')
python_command = f"python id3gini.py -i 7 -C party3_0.ini"
command = f"cd /d {folder_path} && {python_command}"
current_os = platform.system()
ret = subprocess.run(command,stdout=subprocess.PIPE, shell=True, encoding='utf-8')
output = ret.stdout.splitlines()
outputInLines = []
sign = False
for s in output:
    if not sign:
        if s == 'TreeOutPutStartBelow':
            sign = True
    else:
        outputInLines.append(s)
outputInLines.pop() # 弹出第一行空格
output = '\n'.join(outputInLines)
print("计算结果：", output)

features=['Gender','Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History','Property_Area']
# 尝试将结果变成决策树模型
modeltxtRecord.save_txt_file(output)
# text2model.saveModel(output)
