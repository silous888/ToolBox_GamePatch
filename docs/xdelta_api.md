## xdelta_api.py

This file has two functions: one to create a patch, and the other to apply the patch. You need to download xdelta exe in order to use this file. You can download it [here](https://github.com/jmacd/xdelta-gpl/releases).

xdelta is a command line software to create a patch that you can share with everyone, instead of sharing the whole file patched. The patch file will be lighter than the file patched. Also, in the context of game modification, it could be safer to send a file to modify a game file, than the game file modified.

After you download the exe file, put it in the folder where you run your code. But if you want to put xdelta somewhere else, you can, but you need to change its path with the function :

```python
define_xdelta_path(path)
    """redefine path for location of xdelta3.exe,

    Args:
        path (str): path of the folder where xdelta3.exe is

    Returns:
        int: 0 if xdelta3.exe has been found in this path, -1 otherwise, but the path will still be change
    """
```

The first function you would like to use is the one to create a patch file

```python
create_patch(original_file, patched_file, name_patch_file="", patch_path="", overwrite=True)
    """Create a xdelta3 patch file

    Args:
        file_no_patch (str): original file path
        file_patched (str): patched file path, so original file with modifications
        name_patch_file (str, optional): patch file name without ".xdelta" part. Defaults, name of file_no_patch.
        path_patch (str, optional): path of patch file. Defaults to exec repertory.
        overwrite (bool, optional): overwrite or not patch file. Defaults to True.

    Returns:
        int: 0 if the patch file is created, otherwise, return an error code.

    error code:
    -1 if XDELTA_PATH is not valid
    -2 if "original_file" is not found or is not a file
    -3 if "patched_file" is not found or is not a file
    -4 if the path in "patch_path" doesn't exist, or is not a folder
    -5 if xdelta exe not found
    -6 if overwrite is set to False, and the command can't overwrite an existing file
    """
```
```python
# Example:
create_patch("original\\game.exe", "game_translated.exe", patch_path="patch\\", overwrite=True)

# Output:
# Will create a file game.xdelta in the folder "patch"
```

The second function is to apply the patch created.

```python
apply_patch(file_to_patch, patch_file, name_patched_file="")
    """Create a xdelta3 patch file

    Args:
        file_no_patch (str): original file path
        file_patched (str): patched file path, so original file with modifications
        name_patch_file (str, optional): patch file name without ".xdelta" part. Defaults, name of file_no_patch.
        path_patch (str, optional): path of patch file. Defaults to exec repertory.
        overwrite (bool, optional): overwrite or not patch file. Defaults to True.

    Returns:
        int: 0 if the patch file is created, otherwise, return an error code.

    error code:
    -1 if Xdelta3.exe is not found
    -2 if "file_to_patch" is not found or is not a file
    -3 if "patch_file" is not found or is not a file
    -4 if the command has a problem
    -5 if xdelta exe not found
    """
```
```python
# Example:
apply_patch("game.exe", "patch\\game.xdelta")

# Output:
# will patch game.exe, so, will overwrite original file.
```