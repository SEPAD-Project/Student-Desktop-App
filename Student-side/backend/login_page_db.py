import sys
from pathlib import Path
# adding folder to path
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir / "database-code"))

from searching import search_value # type: ignore


def check_auth(username, password):
    print('entered to check auth')
    result = search_value(value=username)
    print(f'this is result {result}')
    print(f'search result is {result}')
    print(f'getted password is {password}')
    if result[2] == password:
        return [True, result]
    else:
        return False

