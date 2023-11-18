import winreg
import os
import shutil


def find_steam_folder_path() -> (str | int):
    """Find where steam is located on windows

    Returns:
        str | int: path of steam, or error code

    error code:<br>
    -1 if path of steam not found in register

    """
    KEY_PATH_STEAM = r"SOFTWARE\\Valve\\Steam"
    KEY_NAME = "SteamPath"
    try:
        key_steam = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH_STEAM, 0, winreg.KEY_READ)
        return winreg.QueryValueEx(key_steam, KEY_NAME)[0]
    except IOError:
        return -1


def find_steam_library_folders_path() -> (list[str] | int):
    """Find every steam game library

    Returns:
        list(str) | int: list with every library folders, or error code

    error code:<br>
    -1 if path of steam not found in register<br>
    -2 if libraryfolders.vdf not found
    """
    def __extract_path_in_textline(line) -> (str | None):
        """find library path in a libraryfolders.vdf line

        Args:
            line (str): line of libraryfolders.vdf

        Returns:
            str | None: path of a game folder,or None if no path in the line
        """
        if line.find("path") == -1:
            return None

        quote_mark_count = 0
        start_index = 0
        end_index = 0
        for index, character in enumerate(line):
            if character == '"':
                quote_mark_count += 1
                if quote_mark_count == 3:
                    start_index = index + 1
                if quote_mark_count == 4:
                    end_index = index
        return line[start_index:end_index].replace("\\\\", "\\")

    # Start of find_steam_library_folders
    steam_folder = find_steam_folder_path()
    if isinstance(steam_folder, int):
        return -1
    game_folders = []
    file_libraryfolders = steam_folder + "\\steamapps\\libraryfolders.vdf"
    if os.path.exists(file_libraryfolders):
        with open(file_libraryfolders, "r") as file:
            for line in file:
                path_library = __extract_path_in_textline(line)
                if path_library is not None:
                    game_folders.append(path_library)
    else:
        return -2
    return game_folders


def find_game_path(game_folder_name) -> (str | int):
    """find path of a steam game

    Args:
        game_folder_name (str): exact name of the steam game folder

    Returns:
        str | int: path of the folder game, or error code

    error code:<br>
    -1 if path of steam not found in register<br>
    -2 if libraryfolders.vdf not found<br>
    -3 if game not found in steam libraries<br>
    -4 game_folder_name not a string
    """
    if not isinstance(game_folder_name, str):
        return -4
    library_folders = find_steam_library_folders_path()
    if isinstance(library_folders, int):
        return library_folders

    EXTRA_PATH = "\\steamapps\\common\\"
    for folder in library_folders:
        full_path = folder + EXTRA_PATH + game_folder_name
        if os.path.exists(full_path):
            return full_path
    return -3


def copy_data_in_steam_game_folder(game_folder_name, data_to_copy, overwrite=True) -> int:
    """copy file of folder in a specific steam game folder

    Args:
        game_folder_name (str): exact name of the steam game folder
        data_to_copy (str): file of folder to copy
        overwrite (bool, optional): overwrite or not if data already exists. Defaults to True.

    Returns:
        int: 0 if finshed without error, error code if not 0

    error code:<br>
    -1 if path of steam not found in register<br>
    -2 if libraryfolders.vdf not found<br>
    -3 if game not found in steam libraries<br>
    -4 game_folder_name not a string<br>
    -5 data_to_copy path does not exist
    """
    if not os.path.exists(data_to_copy) or not isinstance(data_to_copy, str):
        return -5
    game_path = find_game_path(game_folder_name)
    if isinstance(game_path, int):
        return game_path
    if (os.path.isfile(data_to_copy) and (overwrite or
       not os.path.exists(os.path.join(game_path, os.path.basename(data_to_copy))))):
        shutil.copy(data_to_copy, game_path)

    for root, _, files in os.walk(data_to_copy):
        paste_folder = os.path.join(game_path, root[len(data_to_copy):].lstrip("\\"))
        print(paste_folder)
        if not os.path.exists(paste_folder):
            os.makedirs(paste_folder)
        for file in files:
            if overwrite or not os.path.exists(os.path.join(paste_folder, file)):
                shutil.copy(os.path.join(root, file), paste_folder)
    return 0


def copy_data_from_steam_game_folder(game_folder_name, dest, data_to_copy="", overwrite=True) -> int:
    """copy file or folder from a specific steam game folder in a dest folder

    Args:
        game_folder_name (str): exact name of the steam game folder
        dest (str): folder where data will be copy
        data_to_copy (str, optional): file or folder in steam game folder to copy. Defaults to "", so whole game folder.
        overwrite (bool, optional): overwrite or not if data already exists. Defaults to True.

    Returns:
        int: 0 if finshed without error, error code if not 0

    error code:<br>
    -1 if path of steam not found in register<br>
    -2 if libraryfolders.vdf not found<br>
    -3 if game not found in steam libraries<br>
    -4 game_folder_name not a string<br>
    -5 dest path does not exist<br>
    -6 data_to_copy not a string<br>
    -7 data_to_copy does not exist
    """
    if not os.path.exists(dest) or not isinstance(dest, str):
        print(not os.path.exists(dest))
        print(not isinstance(dest, str))
        return -5
    if not isinstance(data_to_copy, str):
        return -6
    game_path = find_game_path(game_folder_name)
    if isinstance(game_path, int):
        return game_path
    if not os.path.exists(os.path.join(game_path, data_to_copy)):
        return -7
    path_data_to_copy = os.path.join(game_path, data_to_copy)
    if (os.path.isfile(data_to_copy) and (overwrite or
       (not os.path.exists(os.path.join(dest, os.path.basename(data_to_copy)))))):
        shutil.copy(data_to_copy, dest)

    for root, _, files in os.walk(path_data_to_copy):
        paste_folder = os.path.join(dest, root[len(path_data_to_copy):])
        print(paste_folder)
        if not os.path.exists(paste_folder):
            os.makedirs(paste_folder)
        for file in files:
            if overwrite or not os.path.exists(os.path.join(paste_folder, file)):
                shutil.copy(os.path.join(root, file), paste_folder)
    return 0