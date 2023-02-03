import smtplib
from email.message import EmailMessage
import string
import random

def send_email(target, title, name):
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
    code = random_code()
    msg.set_content('IIIXR LAB에 오신 것을 환영합니다! \n여기에 귀하의 액세스 코드가 있습니다: ' + code + '\n이 코드를 누구와도 공유하지 마십시오.')

    # 보내는 사람
    msg['From'] = name

    # 받는 사람
    msg['To'] = target

    smtp_gmail.send_message(msg)
    return code

def random_code():
    _LENGTH = 6  # 몇자리?
    string_pool = string.digits  # "0123456789"
    result = ""  # 결과 값
    for i in range(_LENGTH):
        # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다.
        result += random.choice(string_pool)

    return result