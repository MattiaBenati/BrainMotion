# BrainMotion

Desktop image-based word guessing application developed in Python with PySide6, Qt Designer, and PyInstaller packaging support.

![Python](https://img.shields.io/badge/Python-Programming-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![Qt Designer](https://img.shields.io/badge/UI-Qt%20Designer-lightgrey)
![PyInstaller](https://img.shields.io/badge/Packaging-PyInstaller-orange)
![Desktop App](https://img.shields.io/badge/Application-Desktop%20App-informational)

## Demo

https://github.com/user-attachments/assets/e1700a53-a6f9-480f-bf14-ef25510cbe14

## What is it?

BrainMotion is a desktop application that generates word guessing exercises from image files selected by the user.

The software allows the user to choose a folder containing images, extracts the target words from the image file names, and displays each image together with a partially hidden word pattern.

The user must type the correct singular form associated with the displayed image. The application manages difficulty levels, vowel visualization, answer validation, navigation between items, progress tracking, and reset functionality through a graphical interface.

The project is organized into separate modules for application configuration, UI loading, controller logic, game state management, and pure game logic operations.

## Features

- Desktop graphical user interface
- Folder selection through a file dialog
- Automatic image loading from a selected folder
- Support for `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, and `.webp` image files
- Automatic word generation from image file names
- User input normalization
- Word pattern generation with hidden characters
- Optional vowel-based visualization
- Difficulty levels: Easy, Medium, and Hard
- Randomized image order
- Navigation between exercises
- Progress bar for exercise tracking
- Reset option for restarting the current session
- Warning message when no supported images are found
- Custom application icon
- PyInstaller `.spec` file for executable generation
- Modular Python source code organization

## Key Technical Aspects

- PySide6-based desktop interface
- Qt Designer `.ui` file loaded dynamically at runtime
- Controller-based architecture for connecting UI events to application logic
- Centralized runtime state management through a dataclass
- Immutable configuration object for shared application settings
- Image folder scanning using supported file extensions
- File name sanitization to generate target words
- User input normalization for answer comparison
- Randomized reveal order for hidden word characters
- Difficulty-based pre-reveal logic
- Optional vowel pattern visualization
- Resource path handling for both development and packaged execution
- PyInstaller configuration for generating a windowed executable
- Clear separation between UI loading, game state, controller logic, and game logic

## Technology Stack

- Python
- PySide6
- Qt Designer
- Qt `.ui` files
- PyInstaller
- pathlib
- dataclasses
- regular expressions
- random module
- PyCharm or another Python-compatible IDE

## Requirements

- Python 3.10 or later
- PySide6
- PyInstaller, only if building the executable
- Windows, macOS, or Linux with Python and PySide6 support

The packaged executable configuration is designed for Windows.

## Quick Start

### Clone the repository

```bash
git clone https://github.com/MattiaBenati/BrainMotion.git
cd BrainMotion
```

### Install dependencies

Install PySide6:

```bash
pip install PySide6
```

Install PyInstaller only if you want to generate the executable:

```bash
pip install pyinstaller
```

### Run the application

Run the application from source:

```bash
python src/main.py
```

### Build the executable

Build the executable using the existing PyInstaller specification file:

```bash
pyinstaller BrainMotion.spec
```

The generated executable will be created inside the `dist/` directory.

## Usage

1. Start the application
2. Click the `Folder` button
3. Select a folder containing supported image files
4. The software loads the images and generates target words from their file names
5. Select the desired difficulty level
6. Enable or disable vowel visualization
7. Type the answer in the input field
8. Press `Enter` to submit the answer
9. Use `Next` and `Back` to navigate between exercises
10. Use `Reset` to restart the current session with the same selected folder

## Controls

| Control | Action |
| --- | --- |
| `Folder` | Select an image folder |
| `Reset` | Restart the current session |
| `Back` | Move to the previous image |
| `Next` | Move to the next image |
| `Easy` | Use the easiest word reveal level |
| `Medium` | Use the intermediate word reveal level |
| `Hard` | Use the hardest word reveal level |
| `Enabled` | Enable vowel-based visualization |
| `Disabled` | Disable vowel-based visualization |
| Answer field + `Enter` | Submit the typed answer |

## Project Structure

```text
BrainMotion/
├── BrainMotion.spec
└── src/
    ├── assets/
    │   ├── icon.ico
    │   └── icon.png
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── controller.py
    │   ├── game_logic.py
    │   └── game_state.py
    ├── ui/
    │   ├── __init__.py
    │   ├── ui_loader.py
    │   └── window.ui
    └── main.py
```

## Architecture Overview

The project follows a modular Python structure with a clear separation between interface loading, controller logic, application state, and game logic.

- `src/main.py`: starts the application, loads the UI file, sets the application icon, creates the controller, and launches the event loop
- `src/core/config.py`: stores immutable application configuration, including the application name, UI path, icon path, and warning messages
- `src/core/controller.py`: connects UI widgets to application behavior, manages user interactions, updates the interface, and coordinates the application state
- `src/core/game_logic.py`: contains pure logic functions for image scanning, word sanitization, input normalization, vowel detection, word pattern creation, reveal order generation, and difficulty handling
- `src/core/game_state.py`: defines the mutable application state used during a session
- `src/ui/ui_loader.py`: loads the Qt Designer `.ui` file using `QUiLoader`
- `src/ui/window.ui`: defines the graphical interface layout
- `src/assets/`: contains the application icon files
- `BrainMotion.spec`: defines the PyInstaller build configuration for packaging the software as a desktop executable

## Output

The software displays a graphical desktop interface built with PySide6.

During execution, it shows the selected image, the generated hidden word pattern, the answer input field, difficulty controls, vowel visualization options, navigation buttons, reset controls, and progress tracking.

The application does not generate external output files. It processes the selected image folder and displays the generated exercises directly inside the graphical interface.
