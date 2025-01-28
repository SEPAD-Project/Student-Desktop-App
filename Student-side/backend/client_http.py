import requests
import time

curr_time = time.strftime("%H:%M:%S", time.localtime())

# info
username = 'testus'
password = 'supsec'
school_name = 'SchoolA'
class_code = 'Class1'
text_to_send = "sended txt by user"

# server url
server_url = "http://127.0.0.1:5000/upload_text"

# sending data func
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
        print('Sended')
    else:
        print('Error')

# sending data each 30s
# while True:
#     send_data_to_server(username, password, school_name, class_code, text_to_send)
#     time.sleep(30)
