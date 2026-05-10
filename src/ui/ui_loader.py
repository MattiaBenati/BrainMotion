from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMainWindow

def load_ui(uiPath:Path)->QMainWindow:
    """
    Loads a Qt Designer .ui file and returns the main window instance.

    Opens the specified UI file in read-only mode, uses QUiLoader to build
    the interface, and raises a runtime error if loading fails.

    Parameters:
    - uiPath (Path): path to the .ui file

    Returns:
    - QMainWindow: loaded main window instance
    """
    loader=QUiLoader()
    uiFile=QFile(str(uiPath))
    if not uiFile.open(QFile.ReadOnly):
        raise RuntimeError(f"Cannot open UI file: {uiPath}")
    window=loader.load(uiFile,None)
    uiFile.close()
    if window is None:
        raise RuntimeError("Failed to load UI")
    return window
