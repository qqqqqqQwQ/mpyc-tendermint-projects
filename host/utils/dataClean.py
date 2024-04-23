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
        return income
    if income < 1000:
        return 'A'
    elif income < 2000:
        return 'B'
    elif income < 3000:
        return 'C'
    elif income < 4000:
        return 'D'
    elif income < 5000:
        return 'E'
    elif income < 6000:
        return 'F'
    elif income < 7000:
        return 'G'
    elif income < 8000:
        return 'H'
    elif income < 9000:
        return 'I'
    elif income < 10000:
        return 'J'
    elif income < 15000:
        return 'K'
    elif income < 20000:
        return 'L'
    else:
        # 尝试将值转换为数字，如果失败则返回空
        try:
            income_numeric = pd.to_numeric(income)
        except:
            return pd.NA
        return 'M'

def map_amount_range(amount):
    if pd.isna(amount):  # 如果值为空，则不处理
        return amount
    if amount < 100:
        return 'A'
    elif amount < 200:
        return 'B'
    elif amount < 300:
        return 'C'
    elif amount < 400:
        return 'D'
    elif amount < 500:
        return 'E'
    elif amount < 600:
        return 'F'
    elif amount < 700:
        return 'G'
    elif amount < 800:
        return 'H'
    elif amount < 900:
        return 'I'
    elif amount < 1000:
        return 'J'
    elif amount < 1500:
        return 'K'
    elif amount < 2000:
        return 'L'
    else:
        # 尝试将值转换为数字，如果失败则返回空
        try:
            income_numeric = pd.to_numeric(amount)
        except:
            return pd.NA
        return 'M'

def map_amount_term_range(term):
    if pd.isna(term):  # 如果值为空，则不处理
        return term
    if term < 180:
        return 'A'
    elif term < 360:
        return 'B'
    elif term < 540:
        return 'C'
    elif term < 720:
        return 'D'
    elif term < 900:
        return 'E'
    elif term < 1080:
        return 'F'
    elif term < 1260:
        return 'G'
    elif term < 1440:
        return 'H'
    elif term < 1620:
        return 'I'
    elif term < 1800:
        return 'J'
    else:
        # 尝试将值转换为数字，如果失败则返回空
        try:
            income_numeric = pd.to_numeric(term)
        except:
            return pd.NA
        return 'M'


def process_excel_file(df: object) -> object:
    # 清除不需要的列
    # df = df.drop(columns=['不需要的列1', '不需要的列2'])

    # 数字类型数据转换成离散的类别
    df['ApplicantIncome'] = df['ApplicantIncome'].apply(map_income_range)
    df['CoapplicantIncome'] = df['CoapplicantIncome'].apply(map_income_range)
    df['LoanAmount'] = df['LoanAmount'].apply(map_amount_range)
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].apply(map_amount_term_range)
    return df


if __name__ == '__main__':
    file_path = 'path/to/your/uploaded/file.xlsx'
    processed_data = process_excel_file(file_path)
    print(processed_data)