import sys
from pathlib import Path
# adding folder to path
parent_dir = Path(__file__).resolve().parent.parent.parent
print(parent_dir)
sys.path.append(str(parent_dir / "database-code"))

from searching import search_value 


def check_auth(username, password, person):

    print(username)
    try:
        result = search_value(value=username, person=person)
    except Exception as e:
        return [False, e]
    print(result)
    if result != 'not found' :
        if result[2] == password:
            return [True, result]
        else:
            return [False, 'Wrong Pass']
    else:
        return [False, 'Wrong Username']
