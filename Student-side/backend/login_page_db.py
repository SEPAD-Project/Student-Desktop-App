import sys
from pathlib import Path
# adding folder to path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir / "database-code"))

from searching import search_value # type: ignore


def check_auth(username, password):
    result = search_value(value=username)
    if result != 'not found' :
        if result[2] == password:
            return [True, result]
        else:
            return [False, 'Wrong Pass']
    else:
        return [False, 'Wrong Username']

