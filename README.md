# ToolBox_GamePatch

The purpose of this repository is to provide scripts, APIs, and software to facilitate the creation of patches for games, especially translation patches. The repository will be updated with new content from time to time.

Files in the **API** folder contain functions to assist programmers in various tasks, such as simplifying game patching or interacting with Google Drive, Sheets, etc.

In the **doc** folder, you will find HTML documentation for every file in the **API**.

### Short Description of Every Element

**steamGameAPI.py**: Functions to automatically locate specific Steam game folders and copy content to or from them.

**xdeltaAPI**: Functions to create and apply patch with xdelta.

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

## xdeltaAPI.py

This file has two functions: one to create a patch, and the other to apply the patch. You need to download xdelta exe in order to use this file. You can download it [here](https://github.com/jmacd/xdelta-gpl/releases).

xdelta is a command line software to create a patch that you can share with everyone, instead of sharing the whole file patched. The patch file will be lighter than the file patched. Also, in the context of game modification, it could be safer to send a file to modify a game file, than the game file modified.

After you download the exe file, put it in the folder where you run your code. But if you want to put xdelta somewhere else, you can, but you need to change its path with the function :

```python
define_xdelta_path(path)

# will return -1 if path doesn't exist
```

The first function you would like to use is the one to create a patch file

```python
create_patch(original_file, patched_file, name_patch_file="", patch_path="", overwrite=True)

# original_file: path of the original file
# patched_file: path of an original file modified
# name_patch_file: name of xdelta file generated. By default, same as original file
# patch_file: where the patch file will be. By default, in the exec folder
# overwrite: to overwrite xdelta file if one already exists.
```
```python
# Example:
create_patch("original\\game.exe", "game_translated.exe", patch_path="patch\\", overwrite=True)

# Output:
# Will create a file game.xdelta in the folder "patch"

# Returns 0 if there is no error. If an error occurs, refer to the documentation to understand the reason.
```

The second function is to apply the patch created.

```python
apply_patch(file_to_patch, patch_file, name_patched_file="")

# file_to_patch: path of the original file 
# patch_file: path of the xdelta patch file
# name_patch_file: name of xdelta file generated. By default, same as original file
# name_patched_file: name of the file patched generated. By default, WARNING, will overwrite the original file, so same name.
```
```python
# Example:
apply_patch("game.exe", "patch\\game.xdelta")

# Output:
# will patch game.exe, so, will overwrite original file.

# Returns 0 if there is no error. If an error occurs, refer to the documentation to understand the reason.
```