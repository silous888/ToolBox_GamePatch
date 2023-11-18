from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials as sac
import os

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

MAX_RETRIES = 100
WAIT_TIME = 5

IS_CREDENTIAL_FILE_EXISTS = True
IS_CREDENTIAL_CORRECT = True


if os.path.exists("credentials.json"):
    try:
        credentials = sac.from_json_keyfile_name('credentials.json', scope)
        gc = authorize(credentials)
    except Exception:
        IS_CREDENTIAL_CORRECT = False
else:
    IS_CREDENTIAL_FILE_EXISTS = False


# a = gc.open("test").get_worksheet(0)
print(IS_CREDENTIAL_CORRECT)
print(IS_CREDENTIAL_FILE_EXISTS)
