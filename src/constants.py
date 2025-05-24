import os
from pathlib import Path
from enum import IntEnum

appdata = os.environ["AppData"]
db_file = Path(appdata) / "PasswordManager" / "vault.db"
db_file.parent.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = f"sqlite:///{db_file}"
ITERATIONS = 100_000
LOGOUT_TIME = 300_000

class Pages(IntEnum):
    LOGIN_PAGE_CREATE = 0,
    LOGIN_PAGE_EXISTS = 1,
    MAIN_PAGE = 2