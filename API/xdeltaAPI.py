import subprocess as sp
import os

XDELTA_PATH = ""
XDELTA = "xdelta3"


def define_xdelta_path(path):
    global XDELTA_PATH
    if not path.endswith(os.path.sep):
        path = os.path.join(path, '')
    XDELTA_PATH = path
    if not os.path.exists(XDELTA_PATH + "xdelta3.exe"):
        return -1
    return 0


def create_patch(original_file, patched_file, name_patch_file="", patch_path="", overwrite=True):
    """Create a xdelta3 patch file

    Args:
        file_no_patch (str): original file path
        file_patched (str): patched file path, so original file with modifications
        name_patch_file (str, optional): patch file name without ".xdelta" part. Defaults name of file_no_patch.
        path_patch (str, optional): path of patch file. Defaults to exec repertory.
        overwrite (bool, optional): overwrite or not patch file. Defaults to True.

    Returns:
        _type_: _description_
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


def apply_patch():
    """by default, overwrite the file
    otherwise, specify the name of the patched file
    return error code if trying to patch a wrong file
    """
    pass
