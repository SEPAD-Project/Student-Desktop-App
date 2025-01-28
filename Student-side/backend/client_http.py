# import requests
# import time

# # اطلاعات کاربر (فرض می‌کنیم این مقادیر قبلاً تنظیم شده‌اند)
# username = "user1"
# password = "password123"
# school = "SchoolA"
# class_code = "Class101"

# # URL سرور
# server_url = "127.0.0.1:5000"

# # تابع ارسال داده به سرور
# def send_text_to_server(text):
#     try:
#         data = {
#             "username": username,
#             "password": password,
#             "school": school,
#             "class_code": class_code,
#             "text": text
#         }
#         response = requests.post(server_url, json=data)
#         if response.status_code == 200:
#             print(f"Text sent successfully: {response.json()}")
#         else:
#             print(f"Failed to send text. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error while sending data: {e}")

# # شبیه‌سازی ارسال متن هر 30 ثانیه یکبار
# while True:
#     text = input("Enter the text to send: ")  # متنی که کاربر وارد می‌کند
#     send_text_to_server(text)
#     time.sleep(30)







import requests
import time

# اطلاعات مربوط به کاربر
username = 'testus'
password = 'supsec'
school_name = 'SchoolA'
class_code = 'Class1'
text_to_send = "sended txt by user"

# اطلاعات سرور
server_url = "http://127.0.0.1:5000/upload_text"

# تابع ارسال داده‌ها به سرور
def send_data_to_server(username, password, school_name, class_code, text):
    payload = {
        'username': username,
        'password': password,
        'school_name': school_name,
        'class_code': class_code,
        'text': text
    }
    response = requests.post(server_url, data=payload)
    if response.status_code == 200:
        print('sended')
    else:
        print('Error')

# ارسال داده‌ها هر 30 ثانیه
while True:
    send_data_to_server(username, password, school_name, class_code, text_to_send)
    time.sleep(30)
