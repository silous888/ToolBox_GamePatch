from oauth2client.service_account import ServiceAccountCredentials as _sac
from googleapiclient.discovery import build as _build
from googleapiclient.http import MediaIoBaseDownload as _MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload as _MediaFileUpload

import io as _io
import os as _os

try:
    from credentials import credentials_info as _credentials_info
    _MODULE_EXIST = True
except ImportError:
    _MODULE_EXIST = False

_scope = ["https://www.googleapis.com/auth/drive"]

_is_credentials_file_exists = True
_is_credentials_correct = True

_credentials_email = None
_drive_service = None


def __init() -> int:
    """init access to google drive

    Returns:
        int: 0 if access are given, otherwise, return an error code.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct
    """
    global _is_credentials_correct
    global _is_credentials_file_exists
    global _drive_service
    global _credentials_email
    if _drive_service is None:
        if _MODULE_EXIST:
            try:
                credentials = _sac.from_json_keyfile_dict(_credentials_info, _scope)
                _credentials_email = credentials.service_account_email
                _drive_service = _build('drive', 'v3', credentials=credentials)
                _is_credentials_correct = True
            except Exception:
                _is_credentials_correct = False
        elif _os.path.exists("credentials.json"):
            try:
                credentials = _sac.from_json_keyfile_name('credentials.json', _scope)
                _credentials_email = credentials.service_account_email
                _drive_service = _build('drive', 'v3', credentials=credentials)
                _is_credentials_correct = True
            except Exception:
                _is_credentials_correct = False
        else:
            _is_credentials_file_exists = False
    if not _is_credentials_file_exists:
        return -1
    if not _is_credentials_correct:
        return -2
    return 0


def list_files() -> (list[list[str]] | int):
    """give the list of every element the gmail adress has access.

    Returns:
        list(list(str,3)): list with for each element, 0: name, 1: id, 2: type. Error code otherwise

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct
    """
    ret = __init()
    if ret != 0:
        return ret
    results = _drive_service.files().list().execute()
    files = results.get('files', [])
    file_info_list = []

    for file in files:
        file_info_list.append([
            file.get('name', 'N/A'),
            file.get('id', 'N/A'),
            file.get('mimeType', 'N/A')
        ])
    return file_info_list


def get_id_by_name(name_element) -> (str | int):
    """get the id by the name of a file or folder

    Args:
        name_element (str): name of the element

    Returns:
        (str | int): id of the element. Error code otherwise.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if no element with this name
    -4 if more than one element with this name
    """
    ret = __init()
    if ret != 0:
        return ret
    query = f"name='{name_element}'"
    results = _drive_service.files().list(q=query).execute()
    files = results.get('files', [])
    if len(files) == 1:
        return files[0]['id']
    if len(files) == 0:
        return -3
    if (len(files)) > 1:
        return -4


def download_file(file_id, local_folder=".\\") -> int:
    """download a file from google drive, by id.
    Can download every binary file (so png, txt, bin, ...).
    for google files, can download sheet as excel and doc as word.
    for folder, try function download_files_in_folder.

    Args:
        file_id (str): id of the file
        local_folder (str, optional): path where the file will be. Defaults to ".\\".

    Returns:
        int: 0 if no problem. Error code otherwise

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if local_folder doesn't exist<br>
    -4 if file_id not correct<br>
    -5 if file can't be downloaded(slide, forms, ...)
    """
    def google_sheet_as_excel(file_metadata, local_folder):
        local_path = _os.path.join(local_folder, file_metadata['name'] + '.xlsx')
        export_params = {'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        request = _drive_service.files().export_media(fileId=file_metadata['id'], mimeType=export_params['mimeType'])
        return request, local_path

    def google_doc_as_word(file_metadata, local_folder):
        local_path = _os.path.join(local_folder, file_metadata['name'] + '.docx')
        export_params = {'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        request = _drive_service.files().export_media(fileId=file_metadata['id'], mimeType=export_params['mimeType'])
        return request, local_path

    ret = __init()
    if ret != 0:
        return ret

    if not _os.path.exists(local_folder):
        return -3

    try:
        file_metadata = _drive_service.files().get(fileId=file_id).execute()
    except Exception:
        return -4

    if file_metadata['mimeType'].startswith('application/vnd.google-apps'):
        if 'application/vnd.google-apps.spreadsheet' in file_metadata['mimeType']:
            request, local_path = google_sheet_as_excel(file_metadata, local_folder)
        elif 'application/vnd.google-apps.document' in file_metadata['mimeType']:
            request, local_path = google_doc_as_word(file_metadata, local_folder)
        else:
            return -5
    else:
        request = _drive_service.files().get_media(fileId=file_id)
        file_name = file_metadata['name']
        local_path = _os.path.join(local_folder, file_name)

    with _io.FileIO(local_path, 'wb') as fh:
        downloader = _MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return 0


def download_files_in_folder(folder_id, local_folder=".\\", keep_folders=False) -> int:
    """download everything in a google drive folder

    Args:
        folder_id (str): id of the folder
        local_folder (str, optional): path of the folder where the content downloaded will be. Defaults to ".\".
        keep_folders (bool, optional): True to keep folders structure, False to download files only . Defaults to False.

    Returns:
        int: 0 if no problem. Error code otherwise

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if local_folder doesn't exist<br>
    -4 if file_id not correct<br>
    -5 if file can't be downloaded(slide, forms, ...)
    """
    ret = __init()
    if ret != 0:
        return ret

    try:
        results = _drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='files(id, name, mimeType)'
        ).execute()
    except Exception:
        return -4

    files = results.get('files', [])
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if keep_folders:
                new_local_folder = _os.path.join(local_folder, file['name'])
                if not _os.path.exists(new_local_folder):
                    _os.makedirs(new_local_folder)
            else:
                new_local_folder = local_folder
            download_files_in_folder(file['id'], new_local_folder, keep_folders)
        else:
            ret = download_file(file['id'], local_folder)
    return ret


def create_folder(folder_name, id_location) -> (str | int):
    """create a folder in another folder

    Args:
        folder_name (str): name the folder will have
        id_location (str): id of a folder or file where to create the folder.
                           If file, the folder will be in the same folder than this file.

    Returns:
        int: id of the folder created. Error code otherwise.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if parent_folder_id not correct
    """
    ret = __init()
    if ret != 0:
        return ret

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [id_location]
    }
    try:
        folder = _drive_service.files().create(body=folder_metadata, fields='id').execute()
        return folder['id']
    except Exception:
        return -3


def upload_file_or_folder(file_or_folder_path, id_location) -> int:
    """upload a file, or a folder, in the drive id location

    Args:
        file_or_folder_path (str): path of the file or folder to upload
        parent_folder_id (str): id of a folder or file where to create the folder.
                                If file, the folder will be in the same folder than this file.

    Returns:
        int: 0 if no problem. Error code otherwise.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if can't upload a file
    """
    def __upload_file(file_path, parent_folder_id):
        file_metadata = {'name': _os.path.basename(file_path), 'parents': [parent_folder_id]}
        media = _MediaFileUpload(file_path)
        request = _drive_service.files().create(body=file_metadata, media_body=media, fields='id')
        try:
            request.execute()
            return 0
        except Exception:
            return -3

    def __upload_folder(folder_path, parent_folder_id):
        folder_id = create_folder(_os.path.basename(folder_path), parent_folder_id)
        ret = 0
        for elem in _os.listdir(folder_path):
            elem_path = _os.path.join(folder_path, elem)
            if _os.path.isfile(elem_path):
                ret = __upload_file(elem_path, folder_id)
                if ret == -3:
                    return -3
            elif _os.path.isdir(elem_path):
                ret = __upload_folder(elem_path, folder_id)
        return ret

    ret = __init()
    if ret != 0:
        return ret
    if _os.path.isfile(file_or_folder_path):
        ret = __upload_file(file_or_folder_path, id_location)
    else:
        ret = __upload_folder(file_or_folder_path, id_location)
    return ret


def delete_file(file_id) -> int:
    """delete a file or folder in drive,
    only if owned by the service account

    Args:
        file_id (str): id of the element

    Returns:
        int: 0 if no problem. Error code otherwise.

    error code:<br>
    -1 if no credentials file found<br>
    -2 if credentials not correct<br>
    -3 if id incorrect<br>
    -4 if file not owned by the service account
    """
    ret = __init()
    if ret != 0:
        return ret
    try:
        _drive_service.files().delete(fileId=file_id).execute()
        return 0
    except Exception as e:
        if str(e).startswith("<HttpError 403"):
            return -4
        return -3


def delete_all_files_owned_and_not_shared():
    """delete all files owned by the service account, not shared with anyone
    """
    def is_file_owned_and_not_shared(file_id):
        ret = __init()
        if ret != 0:
            return ret

        try:
            file_info = _drive_service.files().get(fileId=file_id, fields='owners,permissions').execute()

            owners = file_info.get('owners', [])
            if len(owners) == 1 and owners[0]['emailAddress'] == _credentials_email:
                permissions = file_info.get('permissions', [])
                if len(permissions) == 1 and permissions[0]['type'] == 'user' and \
                   permissions[0]['emailAddress'] == _credentials_email:
                    return True
        except Exception:
            return -3
        return False

    files = list_files()
    for file in files:
        if is_file_owned_and_not_shared(file[1]):
            delete_file(file[1])
