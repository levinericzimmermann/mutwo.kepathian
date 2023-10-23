import os

PAPERSIZE_TO_WIDTH = {"a4": 21, "a5": 14.8}

_pathbase = "/".join(os.path.abspath(__file__).split("/")[:-1])
TEMPLATE_PATH = f"{_pathbase}/templates"
SILEEXT_PATH = f"{_pathbase}/sileext"

del _pathbase, os
