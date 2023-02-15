import pandas as pd
import smtplib
import string
import random
from email.message import EmailMessage

class UserInfo():
    def __init__(self):
        self.DB = self.set_DB()

    def set_DB(self):
        try:
            self.DB = pd.read_csv('./utils/db.csv', low_memory=False, index_col = 0)
        except:
            self.DB = pd.DataFrame(columns=['name', 'email', 'random_code', 'permission'])
            self.DB.to_csv('./utils/db.csv')

        return self.DB

    def join(self, name):
        temp = pd.DataFrame({'name': [name], 'email': [''], 'random_code': [''], 'permission': ['guest']})
        self.DB = pd.concat([self.DB, temp], ignore_index=True)
        self.DB.to_csv('./utils/db.csv')
        print(f'{name} join')

    def drop(self, name):
        self.DB.drop(self.DB.loc[self.DB['name'] == str(name)].index, inplace=True)
        self.DB.to_csv('./utils/db.csv')

    def set_info(self, name, data_type, data_content):
        self.DB.loc[self.DB['name'] == str(name), data_type] = data_content
        self.DB.to_csv('./utils/db.csv')

    def get_info(self, name, data_type):
        length = len(self.DB.loc[self.DB['name'] == str(name), data_type].values)
        if length == 0:
            return ''
        else:
            return self.DB.loc[self.DB['name'] == str(name), data_type].values[0]

    def send_email(self, target, title, name):
        smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)

        # 서버 연결을 설정하는 단계
        smtp_gmail.ehlo()

        # 연결을 암호화
        smtp_gmail.starttls()

        # 로그인
        smtp_gmail.login('ssw03270@khu.ac.kr', 'tjtmddnjs01')

        msg = EmailMessage()

        # 제목 입력
        msg['Subject'] = title
        # 내용 입력
        code = self.make_random_code()
        msg.set_content('IIIXR LAB에 오신 것을 환영합니다! \n여기에 귀하의 액세스 코드가 있습니다: ' + code + '\n이 코드를 누구와도 공유하지 마십시오.')
        # 보내는 사람
        msg['From'] = name
        # 받는 사람
        msg['To'] = target

        smtp_gmail.send_message(msg)
        return code

    def make_random_code(self):
        _LENGTH = 6  # 몇자리?
        string_pool = string.digits  # "0123456789"
        result = ""  # 결과 값
        for i in range(_LENGTH):
            # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다.
            result += random.choice(string_pool)

        return result