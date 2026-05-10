import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from core.controller import MainWindowController
from ui.ui_loader import load_ui
from core.config import CONFIG

def resource_path(relativePath:Path)->Path:
    """
    Resolves a resource path for both development and packaged execution.

    Returns the PyInstaller temporary path when available, otherwise the src folder.
    """
    basePath=Path(getattr(sys,"_MEIPASS",Path(__file__).resolve().parent))
    return basePath/relativePath

def main()->None:
    """
    Application entry point.
    """
    app=QApplication(sys.argv)
    uiPath=resource_path(CONFIG.uiRelativePath)
    iconPath=resource_path(CONFIG.iconRelativePath)
    window=load_ui(uiPath)
    window.setWindowTitle(CONFIG.appName)
    if iconPath.exists():
        window.setWindowIcon(QIcon(str(iconPath)))
    window.setFixedSize(window.size())
    _controller=MainWindowController(window)
    window.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()