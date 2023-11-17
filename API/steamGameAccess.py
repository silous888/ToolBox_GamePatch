import winreg


def find_steam_folder():
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

