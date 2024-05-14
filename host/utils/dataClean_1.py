import pandas as pd

"""
Gender（性别）： 贷款人的性别，可能是男性或女性。
Married（婚姻状况）： 贷款人的婚姻状况，可能是已婚或未婚。
Dependents（家属数量）： 贷款人家庭中的家属数量，可能是一个整数，表示贷款人有多少个家属。
Education（教育水平）： 贷款人的教育水平，可能是毕业或未毕业。
Self_Employed（自雇情况）： 贷款人是否为自雇人士，可能是自雇或非自雇。
ApplicantIncome（申请人收入）： 贷款申请人的个人收入，通常是一个数值，表示他们每月或每年的收入。
CoapplicantIncome（共同申请人收入）： 贷款申请人的共同申请人的收入，如果有的话。这通常是另一个数值，表示共同申请人每月或每年的收入。
LoanAmount（贷款金额）： 贷款的金额，通常是一个数值，表示申请的贷款额度。
Loan_Amount_Term（贷款期限）： 贷款的期限，即贷款应该在多长时间内还清。通常以月为单位表示。
Credit_History（信用历史）： 贷款人的信用历史，可能是一个二元变量，表示他们是否有良好的信用历史（1表示良好，0表示不良好）。
Property_Area（房产地区）： 贷款人的房产所在地区，可能是城市、郊区或农村。
Loan_Status（贷款状态）： 表示贷款是否批准的标志，可能是一个二元变量，通常是 "Y" 表示批准，"N" 表示未批准。

数据处理：
1.多出来的其他的标签全部清除，缺失的标签先不管，看看多方计算时会怎么样先

"""
def map_income_range(income):
    if pd.isna(income):  # 如果值为空，则不处理
        return -1
    # 尝试将值转换为数字，如果失败则返回空
    try:
        income_numeric = pd.to_numeric(income)
    except:
        return -1
    if income < 1000:
        return 0
    elif income < 2000:
        return 1
    elif income < 3000:
        return 2
    elif income < 4000:
        return 3
    elif income < 5000:
        return 4
    elif income < 6000:
        return 5
    elif income < 7000:
        return 6
    elif income < 8000:
        return 7
    elif income < 9000:
        return 8
    elif income < 10000:
        return 9
    elif income < 15000:
        return 10
    elif income < 20000:
        return 11
    else:
        return 12

def map_amount_range(amount):
    if pd.isna(amount):  # 如果值为空，则不处理
        return 15
    # 尝试将值转换为数字，如果失败则返回空
    try:
        income_numeric = pd.to_numeric(amount)
    except:
        return 15
    if amount < 100:
        return 0
    elif amount < 200:
        return 1
    elif amount < 300:
        return 2
    elif amount < 400:
        return 3
    elif amount < 500:
        return 4
    elif amount < 600:
        return 5
    elif amount < 700:
        return 6
    elif amount < 800:
        return 7
    elif amount < 900:
        return 8
    elif amount < 1000:
        return 9
    elif amount < 1500:
        return 10
    elif amount < 2000:
        return 11
    else:
        return 12

def map_amount_term_range(term):
    if pd.isna(term):  # 如果值为空，则不处理
        return -1
    # 尝试将值转换为数字，如果失败则返回空
    try:
        income_numeric = pd.to_numeric(term)
    except:
        return -1
    if term < 180:
        return 0
    elif term < 360:
        return 1
    elif term < 540:
        return 2
    elif term < 720:
        return 3
    elif term < 900:
        return 4
    elif term < 1080:
        return 5
    elif term < 1260:
        return 6
    elif term < 1440:
        return 7
    elif term < 1620:
        return 8
    elif term < 1800:
        return 9
    else:
        return 10

def map_gender(gender):
    if gender == "Male":
        return 1
    elif gender == "Female":
        return 0
    else:
        return -1

def map_Married(m):
    if m == "Yes":
        return 1
    elif m == "No":
        return 0
    else:
        return -1
def map_Dependents(m):
    if m == "0":
        return 0
    elif m == "1":
        return 1
    elif m == "2":
        return 2
    else:
        return 3
def map_Education(m):
    if m == "Graduate":
        return 0
    elif m == "Not Graduate":
        return 1
    else:
        return 2
def map_Self_Employed(m):
    if m == "No":
        return 0
    elif m == "Yes":
        return 1
    else:
        return 2
def map_Self_Employed(m):
    if m == "No":
        return 0
    elif m == "Yes":
        return 1
    else:
        return 2
def map_Property_Area(m):
    if m == "Rural":
        return 0
    elif m == "Urban":
        return 1
    elif m == "Semiurban":
        return 2
    else:
        return 3
def map_Credit_History(m):
    if m == "0":
        return 0
    elif m == "1":
        return 1
    else:
        return 2
def map_Loan_Status(m):
    if m == "Y":
        return 0
    elif m == "N":
        return 1
    else:
        return 2
def process_excel_file(df: pd.DataFrame) -> pd.DataFrame:
    # 清除不需要的列
    # df = df.drop(columns=['不需要的列1', '不需要的列2'])

    # 数字类型数据转换成离散的类别
    df['Gender'] = df['Gender'].apply(map_gender)
    df['Married'] = df['Married'].apply(map_Married)
    df['Dependents'] = df['Dependents'].apply(map_Dependents)
    df['Education'] = df['Education'].apply(map_Education)
    df['Self_Employed'] = df['Self_Employed'].apply(map_Self_Employed)
    df['Credit_History'] = df['Credit_History'].apply(map_Credit_History)
    df['Property_Area'] = df['Property_Area'].apply(map_Property_Area)
    df['ApplicantIncome'] = df['ApplicantIncome'].apply(map_income_range)
    df['CoapplicantIncome'] = df['CoapplicantIncome'].apply(map_income_range)
    df['LoanAmount'] = df['LoanAmount'].apply(map_amount_range)
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].apply(map_amount_term_range)
    df['Loan_Status'] = df['Loan_Status'].apply(map_Loan_Status)
    return df


if __name__ == '__main__':
    file_path = 'path/to/your/uploaded/file.xlsx'
    processed_data = process_excel_file(file_path)
    print(processed_data)