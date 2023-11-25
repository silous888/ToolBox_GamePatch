from oauth2client.service_account import ServiceAccountCredentials as sac
from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload

import os

try:
    from credentials import credentials_info
    MODULE_EXIST = True
except ImportError:
    MODULE_EXIST = False

scope = ["https://www.googleapis.com/auth/drive"]

MAX_RETRIES = 100
WAIT_TIME = 5

is_credentials_file_exists = True
is_credentials_correct = True

drive_service = None


def __init() -> int:
    """init access to google drive

    Returns:
        int: 0 if access are given, otherwise, return an error code.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct
    """
    global is_credentials_correct
    global is_credentials_file_exists
    global drive_service
    if drive_service is None:
        if MODULE_EXIST:
            try:
                credentials = sac.from_json_keyfile_dict(credentials_info, scope)
                drive_service = build('drive', 'v3', credentials=credentials)
                is_credentials_correct = True
            except Exception:
                is_credentials_correct = False
        elif os.path.exists("credentials.json"):
            try:
                credentials = sac.from_json_keyfile_name('credentials.json', scope)
                drive_service = build('drive', 'v3', credentials=credentials)
                is_credentials_correct = True
            except Exception:
                is_credentials_correct = False
        else:
            is_credentials_file_exists = False
    if not is_credentials_file_exists:
        return -1
    if not is_credentials_correct:
        return -2
    return 0


def list_files() -> (list[list[str]] | int):
    """give the list of every element the gmail adress has access.

    Returns:
        list(list(str,3)): list with for each element, 0: name, 1: id, 2: type
    """
    ret = __init()
    if ret != 0:
        return ret
    results = drive_service.files().list().execute()
    files = results.get('files', [])
    file_info_list = []

    for file in files:
        file_info_list.append([
            file.get('name', 'N/A'),
            file.get('id', 'N/A'),
            file.get('mimeType', 'N/A')
        ])
    return file_info_list
