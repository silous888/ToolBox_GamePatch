import winreg
import os
import shutil


def find_steam_folder_path() -> (str | None):
    """Find where steam is located on windows

    Returns:
        str: path of steam, None if not found
    """
    KEY_PATH_STEAM = r"SOFTWARE\\Valve\\Steam"
    KEY_NAME = "SteamPath"
    try:
        key_steam = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH_STEAM, 0, winreg.KEY_READ)
        return winreg.QueryValueEx(key_steam, KEY_NAME)[0]
    except IOError:
        return None


def find_steam_library_folders_path() -> (list[str] | None):
    """Find every steam game library

    Returns:
        list(str): list with every library folders, None if steam folder or libraryfolders.vdf are not found
    """
    def __extract_path_in_textline(line):
        """find library path in a libraryfolders.vdf line

        Args:
            line (str): line of libraryfolders.vdf

        Returns:
            str : path of a game folder, None if no path in the line
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
    if steam_folder is None:
        return None
    game_folders = []
    file_libraryfolders = steam_folder + "\\steamapps\\libraryfolders.vdf"
    if os.path.exists(file_libraryfolders):
        with open(file_libraryfolders, "r") as file:
            for line in file:
                path_library = __extract_path_in_textline(line)
                if path_library is not None:
                    game_folders.append(path_library)
    else:
        return None
    return game_folders


def find_game_path(game_folder_name) -> (str | None):
    """find path of a steam game

    Args:
        game_folder_name (str): exact name of the steam game folder

    Returns:
        str: path of the folder game, None if not founded, or no library folders
    """
    library_folders = find_steam_library_folders_path()
    if library_folders is None:
        return None

    EXTRA_PATH = "\\steamapps\\common\\"
    for folder in library_folders:
        full_path = folder + EXTRA_PATH + game_folder_name
        if os.path.exists(full_path):
            return full_path
    return None


def copy_data_in_steam_game_folder(game_folder_name, data_to_copy, overwrite=True) -> int:
    game_path = find_game_path(game_folder_name)
    if game_path is None:
        return -1
    if os.path.isfile(data_to_copy) and overwrite:
        shutil.copy(data_to_copy, find_game_path(game_path))

    for root, dirs, files in os.walk(data_to_copy):
        paste_folder = game_path + root[len(data_to_copy):]
        print("paste folder " + paste_folder)
        if not os.path.exists(paste_folder):
            os.makedirs(paste_folder)
        print("root " + root)
        for dir in dirs:
            print("dir " + dir)
        for file in files:
            if overwrite or not os.path.exists(os.path.join(paste_folder, file)):
                shutil.copy(os.path.join(root, file), paste_folder)
    return 0

