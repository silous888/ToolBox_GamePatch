from oauth2client.service_account import ServiceAccountCredentials as sac
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import io
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


def download_file(file_id, local_folder=".\\"):
    """download a file from google drive, by id

    Args:
        file_id (str): id of the file
        local_folder (str, optional): path where the file will be. Defaults to ".\\".
    """
    def google_sheet_as_excel(file_metadata, local_folder):
        local_path = os.path.join(local_folder, file_metadata['name'] + '.xlsx')
        export_params = {'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        request = drive_service.files().export_media(fileId=file_metadata['id'], mimeType=export_params['mimeType'])
        return request, local_path

    def google_doc_as_word(file_metadata, local_folder):
        local_path = os.path.join(local_folder, file_metadata['name'] + '.docx')
        export_params = {'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        request = drive_service.files().export_media(fileId=file_metadata['id'], mimeType=export_params['mimeType'])
        return request, local_path

    ret = __init()
    if ret != 0:
        return ret

    try:
        file_metadata = drive_service.files().get(fileId=file_id).execute()
    except Exception:
        return -3

    if file_metadata['mimeType'].startswith('application/vnd.google-apps'):
        if 'application/vnd.google-apps.spreadsheet' in file_metadata['mimeType']:
            request, local_path = google_sheet_as_excel(file_metadata, local_folder)
        elif 'application/vnd.google-apps.document' in file_metadata['mimeType']:
            request, local_path = google_doc_as_word(file_metadata, local_folder)
        else:
            return -4
    else:
        request = drive_service.files().get_media(fileId=file_id)
        file_name = file_metadata['name']
        local_path = os.path.join(local_folder, file_name)

    with io.FileIO(local_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return 0


def download_files_in_folder(folder_id, local_folder=".\\", keep_folders=False):
    ret = __init()
    if ret != 0:
        return ret

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id, name, mimeType)'
    ).execute()
    files = results.get('files', [])
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if keep_folders:
                new_local_folder = os.path.join(local_folder, file['name'])
                if not os.path.exists(new_local_folder):
                    os.makedirs(new_local_folder)
            else:
                new_local_folder = local_folder
            download_files_in_folder(file['id'], new_local_folder, keep_folders)
        else:
            download_file(file['id'], local_folder)
    return 0
