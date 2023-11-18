# ToolBox_GamePatch

The purpose of this repository is to provide scripts, APIs, and software to facilitate the creation of patches for games, especially translation patches. The repository will be updated with new content from time to time.

Files in the **API** folder contain functions to assist programmers in various tasks, such as simplifying game patching or interacting with Google Drive, Sheets, etc.

In the **doc** folder, you will find HTML documentation for every file in the **API**.

### Short Description of Every Element

**steamGameAccess.py**: This file contains functions to automatically locate specific Steam game folders and copy content to or from them.

## API: steamGameAccess.py

This file includes all the functions necessary to find the location of a Steam game folder and to copy data to or from the game folder. Here is a brief explanation of functions you will likely need, but more details can be found in the HTML documentation.


To use it, download the file and, in your Python script, include the following:

```python
import steamGameAccess as sga
```
You can now access functions in the file using `sga.function_name()`.

Among the available functions, three are particularly useful.

The first one returns the path to the Steam game folder.


```python
def find_game_path(game_folder_name) -> (str | int)
# game_folder_name: Exact name of the game folder in SteamLibrary\steamapps\common\
# Windows paths are case-insensitive, but if possible, provide the name with case sensitivity.
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
# game_folder_name: Same as the first function.
# data_to_copy: path of the file or folder to copy.
# overwrite: If True, overwrite existing data in the game folder. Defaults to True.
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
# game_folder_name: Same as the first function.
# dest: The folder where you want to paste the data.
# data_to_copy: Relative path to the file or folder you want to copy. By default, it copies the entire game folder content.
# overwrite: If True, overwrite existing data in your dest folder. Defaults to True.
```
```python
# Example:
copy_data_from_steam_game_folder("TEKKEN 7", "F:\\Documents\\exe_to_extract\\", "TEKKEN 7.exe")

# Output:
# Will copy the "TEKKEN 7.exe" file to the "exe-to_extract" folder.

# Returns 0 if there is no error. If an error occurs, refer to the documentation to understand the reason.
```
