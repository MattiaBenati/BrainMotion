from dataclasses import dataclass
from typing import Optional

@dataclass
class AppState:
    """
    Container for the mutable application state.

    This dataclass stores all runtime data required to manage the current
    session, including image paths, navigation index, selected folder,
    and word-related structures used by the game logic.
    """
    imagePaths:list[str]
    currentIndex:int
    selectedFolder:Optional[str]
    fullWords:list[str]
    underscoreLines:list[list[str]]
    letterStates:list[list[str]]
    revealOrders:list[list[int]]

    @staticmethod
    def empty()->"AppState":
        """
        Creates and returns an empty application state.

        Initializes all fields with default values, representing the absence
        of an active session.
        """
        return AppState(imagePaths=[],currentIndex=-1,selectedFolder=None,fullWords=[],underscoreLines=[],letterStates=[],revealOrders=[])
