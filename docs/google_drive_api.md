## API: google_drive_api.py

this file includes all the functions necessary to manage files and folders in Google Drive. There are functions for uploading, downloading, deleting elements, and creating folders

You need Google API credentials to use this file. To obtain credentials, refer to this [file](credentials_google_api.md).


To grant access to a file or folder for your service account, you need to share it with the email address associated with the service account.

The first useful functions help determine which elements the service account has access to. The ID is the string of random character in the url, but you can obtain it by using *list_files()* or *get_id_by_name()*.

*has_access_to_element()* will tell you if an element is shared with the service account.

```python
def has_access_to_element(element_id) -> (bool | int):
    """Check if the service account of the credentials has access to an element with the given ID.

    Args:
        element_id (str): ID of the element to check.

    Returns:
        (bool | int): True if access, False if no access. Error code otherwise

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    """


def list_files() -> (list[list[str]] | int):
    """give the list of every element the gmail adress has access.

    Returns:
        (list(list(str,3)) | int): list with for each element, 0: name, 1: id, 2: type. Error code otherwise

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    """


def get_id_by_name(name_element) -> (str | int):
    """get the id by the name of a file or folder

    Args:
        name_element (str): name of the element

    Returns:
        (str | int): id of the element. Error code otherwise.

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if no element with this name
    -4 if more than one element with this name
    """
```


After obtaining the ID, you can download the contents of the drive using two functions.
The *download_file()* function is capable of downloading binary files (PNG, TXT, GIF... but not google collab, slide, etc). Additionally, it can download sheets as Excel files and docs as Word files.

For downloading folders and multiple files in one go, use *download_files_in_folder()*. This function will download only the contents of the folder, not the folder itself.

Consider a scenario where you have a drive folder named "data" containing a sheet, a PNG file, and a subfolder with a JPG file. If you still wish to have everything in a "data" folder on your computer, you need to create the folder and provide its path to the function. If you want to retain the subfolder with the JPG file, and not just download the JPG, you should set *keep_folders* to True. Similar to the previous function, the sheet will be downloaded as an Excel file in this case.

```python
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

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if local_folder doesn't exist
    -4 if file_id not correct
    -5 if file can't be downloaded(slide, forms, ...)
    """


def download_files_in_folder(folder_id, local_folder=".\\", keep_folders=False) -> int:
    """download everything in a google drive folder

    Args:
        folder_id (str): id of the folder
        local_folder (str, optional): path of the folder where the content downloaded will be. Defaults to ".\".
        keep_folders (bool, optional): True to keep folders structure, False to download files only . Defaults to False.

    Returns:
        int: 0 if no problem. Error code otherwise

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if local_folder doesn't exist
    -4 if file_id not correct
    -5 if file can't be downloaded(slide, forms, ...)
    """
```


Now, for the upload part, there is one function that can handle both files and folders.

```python
def upload(file_or_folder_path, id_location) -> int:
    """upload a file, or a folder, in the drive id location

    Args:
        file_or_folder_path (str): path of the file or folder to upload
        parent_folder_id (str): id of a folder or file where to create the folder.
                                If file, the folder will be in the same folder than this file.

    Returns:
        int: 0 if no problem. Error code otherwise.

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if can't upload a file
    """
```

You can also create a Google Drive folder if needed.

```python
def create_folder(folder_name, id_location) -> (str | int):
    """create a folder in another folder

    Args:
        folder_name (str): name the folder will have
        id_location (str): id of a folder or file where to create the folder.
                           If file, the folder will be in the same folder than this file.

    Returns:
        int: id of the folder created. Error code otherwise.

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if parent_folder_id not correct
    """
```

And finally, to delete elements. Currently you can only delete files uploaded by the service account, where the service account is the owner. There are two functions for that.

*delete_file()* will remove the file from your drive, making it invisible to you. However, the service account will still have access to it.<br>
To permanently delete every file deleted with *delete_file()*, use *delete_all_files_owned_and_not_shared()* to clear everything.

```python
def delete_file(file_id) -> int:
    """delete a file or folder in drive,
    only if owned by the service account

    Args:
        file_id (str): id of the element

    Returns:
        int: 0 if no problem. Error code otherwise.

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if id incorrect
    -4 if file not owned by the service account
    """


def delete_all_files_owned_and_not_shared():
    """delete all files owned by the service account, not shared with anyone
    """
```