from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AppConfig:
    """
    Centralized application configuration container.

    This dataclass stores constant values used across the application,
    including UI paths, application metadata, demo settings, and user-facing
    messages. The configuration is immutable to ensure consistency at runtime.
    """
    appName:str="BrainMotion"
    demoWord:str="example"
    uiRelativePath:Path=Path("ui")/"window.ui"
    iconRelativePath:Path=Path("assets")/"icon.png"
    noImagesTitle:str="BrainMotion"
    noImagesText:str="No supported images were found in the selected folder."
    noImagesFormats:str="Supported formats:\nPNG · JPG · JPEG · BMP · GIF · WEBP"


# Creates a single, immutable configuration instance shared across the entire application.
CONFIG=AppConfig()
