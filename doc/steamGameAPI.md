## API: steamGameAPI.py

This file includes all the functions necessary to find the location of a Steam game folder and to copy data to or from the game folder. Here is a brief explanation of functions you will likely need, but more details can be found in the HTML documentation.


To use it, download the file and, in your Python script, include the following:

```python
import steamGameAPI as sga
```
You can now access functions in the file using `sga.function_name()`.

Among the available functions, three are particularly useful.

The first one returns the path to the Steam game folder.


```python
def find_game_path(game_folder_name) -> (str | int)
    """find path of a steam game

    Args:
        game_folder_name (str): exact name of the steam game folder in SteamLibrary\\steamapps\\common\\

    Returns:
        str | int: path of the folder game, or error code

    error code:<br>
    -1 if path of steam not found in register<br>
    -2 if libraryfolders.vdf not found<br>
    -3 if game not found in steam libraries<br>
    -4 game_folder_name not a string
    """
```
```python
# Example:
print(find_game_path("TEKKEN 7"))

# Output:
# F:\Games\SteamLibrary\steamapps\common\TEKKEN 7
```

The second one will copy a file or a folder in the steam game file

```python
def copy_data_in_steam_game_folder(game_folder_name,
                                   data_to_copy,
                                   overwrite=True) -> int
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
```
```python
# Example 1:
copy_in_steam_game_folder("TEKKEN 7", "F:\\Documents\\Patch")

# Output:
# The files and folders within the 'Patch' directory are copied to the TEKKEN 7 game folder, but the 'Patch' directory itself is not copied; only its contents are included.

# Example 2:
copy_in_steam_game_folder("TEKKEN 7", "F:\\Documents\\Patch\\TEKKEN 7.exe", overwrite=False)

# Output:
# If TEKKEN 7.exe already exists in the Steam game folder, nothing will happen.

# Returns 0 if there is no error. If an error occurs, refer to the documentation to understand the reason.
```

The last function that could be useful is to copy a file or folder from the Steam game folder to another location on your computer.

```python
def copy_data_from_steam_game_folder(game_folder_name,
                                     dest,
                                     data_to_copy="",
                                     overwrite=True) -> int
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
```
```python
# Example:
copy_data_from_steam_game_folder("TEKKEN 7", "F:\\Documents\\exe_to_extract\\", "TEKKEN 7.exe")

# Output:
# Will copy the "TEKKEN 7.exe" file to the "exe-to_extract" folder.

# Returns 0 if there is no error. If an error occurs, refer to the documentation to understand the reason.
```