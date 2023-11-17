import winreg
import os


def find_steam_folder() -> (str | None):
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


def find_steam_library_folders() -> (list[str] | None):
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
    steam_folder = find_steam_folder()
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
