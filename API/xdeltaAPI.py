import subprocess as sp
import os
from time import sleep


XDELTA_PATH = ""
"""
path where xdelta3.exe is, use "define_xdelta_path()" to change it<br>
By default, the path is where you run your code
"""

XDELTA = "xdelta3"
"""
xdelta command in shell
"""


def define_xdelta_path(path) -> (int):
    """redefine path for location of xdelta3.exe,

    Args:
        path (str): path of the folder where xdelta3.exe is

    Returns:
        int: 0 if xdelta3.exe has been found in this path, -1 otherwise, but the path will still be change
    """
    global XDELTA_PATH
    if not path.endswith(os.path.sep):
        path = os.path.join(path, '')
    XDELTA_PATH = path
    if not os.path.exists(XDELTA_PATH + "xdelta3.exe"):
        return -1
    return 0


def create_patch(original_file, patched_file, name_patch_file="", patch_path="", overwrite=True) -> (int):
    """Create a xdelta3 patch file

    Args:
        file_no_patch (str): original file path
        file_patched (str): patched file path, so original file with modifications
        name_patch_file (str, optional): patch file name without ".xdelta" part. Defaults, name of file_no_patch.
        path_patch (str, optional): path of patch file. Defaults to exec repertory.
        overwrite (bool, optional): overwrite or not patch file. Defaults to True.

    Returns:
        int: 0 if the patch file is created, otherwise, return an error code.

    error code:<br>
    -1 if Xdelta3.exe is not found<br>
    -2 if "original_file" is not found or is not a file<br>
    -3 if "patched_file" is not found or is not a file<br>
    -4 if the path in "patch_path" doesn't exist, or is not a folder<br>
    -5 if overwrite is set to False, and the command can't overwrite an existing file
    """
    if XDELTA_PATH != "" and not os.path.exists(XDELTA_PATH):
        return -1
    if not os.path.exists(original_file) or not os.path.isfile(original_file):
        return -2
    if not os.path.exists(patched_file) or not os.path.isfile(patched_file):
        return -3
    if patch_path != "" and \
       (not os.path.exists(patch_path) or not os.path.isdir(patch_path)):
        return -4

    if len(name_patch_file) == 0:
        name_patch_file = os.path.splitext(os.path.basename(original_file))[0]
    if not patch_path.endswith(os.path.sep):
        patch_path = os.path.join(patch_path, '')

    command = [
        XDELTA_PATH + XDELTA,
        "-e",  # compress
        "-s",  # source
        original_file,
        patched_file,
        patch_path + name_patch_file + ".xdelta",
    ]
    if overwrite:
        command.insert(1, "-f")
    output = sp.run(command, stdout=sp.PIPE, creationflags=sp.CREATE_NO_WINDOW)
    if output.returncode == 1:
        return -5
    return output.returncode


def apply_patch(file_to_patch, patch_file, name_patched_file="") -> (int):
    """by default, overwrite the file
    otherwise, specify the name of the patched file
    return error code if trying to patch a wrong file
    """
    def overwrite_original_file():
        os.remove(file_to_patch)
        sleep(0.3)
        os.rename(name_patched_file, file_to_patch)

    overwrite = False
    if name_patched_file == "":
        splitname = os.path.splitext(os.path.basename(file_to_patch))
        name_patched_file = os.path.dirname(file_to_patch) + splitname[0] + "n" + splitname[1]
        overwrite = True
    command = [
        XDELTA_PATH + XDELTA,
        "-f",
        "-d",  # uncompress
        "-s",  # source
        file_to_patch,
        patch_file,
        name_patched_file,
    ]
    process = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE,
                     creationflags=sp.CREATE_NO_WINDOW)

    if overwrite and process.returncode == 0:
        overwrite_original_file()
    return process.returncode
