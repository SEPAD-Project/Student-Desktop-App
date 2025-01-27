# from getpass import getpass
# from mysql.connector import connect, Error

# try:
#     with connect(
#         host="localhost",
#         user='root',
#         password='ardbms',  # getpass("Enter password: ")
#     ) as connection:
#         print(connection)
#         create_db_query = "CREATE DATABASE sap"
#         with connection.cursor() as cursor:
#             cursor.execute(create_db_query)
# except Error as e:
#     print(e)




import sys
from pathlib import Path
# adding folder to path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir / "database-code"))
# sys.path.append(str(parent_dir / "Students-side/gui"))
# print(Path(__file__).resolve().parent.parent)

from searching import search_value


def check_auth(username, password):
    print('entered to check auth')
    result = search_value(value=username)
    print(f'search result is {result}')
    print(f'getted password is {password}')
    if result == password:
        return True
    else:
        return False

