import random
from PySide6.QtWidgets import QMainWindow,QLabel,QPushButton,QLineEdit,QProgressBar,QRadioButton,QFileDialog,QMessageBox
from PySide6.QtGui import QPixmap,QPainter
from PySide6.QtCore import Qt
from core.game_state import AppState
from core import game_logic
from core.config import CONFIG

"""
Controller for the main application window (PySide6).

This class binds UI widgets defined in the Qt Designer .ui file, validates
their presence, and connects user interactions (buttons, text input, and
radio toggles) to the application logic.

It coordinates three core responsibilities:
- UI management: updating labels, buttons, progress bar, and image display
- State management: storing and updating the current session via AppState
- Game logic orchestration: delegating pure operations to core.game_logic
  (e.g. word sanitization, reveal rules, difficulty, and vowel patterns)

The controller acts as the bridge between the view (QMainWindow widgets)
and the model/state (AppState), keeping the interface consistent with the
current image, word progress, and selected options.
"""
class MainWindowController:
    def __init__(self,window:QMainWindow)->None:
        self.window=window
        self._bind_widgets(window)
        self._assert_ui()
        self._wire_events()
        self.demoWord=CONFIG.demoWord
        self.state=AppState.empty()
        self._reset_state()
        self._setup_image_label()

    def _bind_widgets(self,window:QMainWindow)->None:
        """
        Connects the UI widgets defined in the Qt Designer file to controller attributes.

        Each widget is retrieved by its objectName using findChild and stored as an
        instance attribute, allowing the controller to access and manipulate the
        interface programmatically.
        """
        self.lblImage:QLabel=window.findChild(QLabel,"lblImage")
        self.lblWordPreview:QLabel=window.findChild(QLabel,"lblWordPreview")
        self.lblWord:QLabel=window.findChild(QLabel,"lblWord")
        self.txtAnswer:QLineEdit=window.findChild(QLineEdit,"txtAnswer")
        self.btnBack:QPushButton=window.findChild(QPushButton,"btnBack")
        self.btnNext:QPushButton=window.findChild(QPushButton,"btnNext")
        self.btnFolder:QPushButton=window.findChild(QPushButton,"btnFolder")
        self.btnReset:QPushButton=window.findChild(QPushButton,"btnReset")
        self.progressBar:QProgressBar=window.findChild(QProgressBar,"progressBar")
        self.rdoEasy:QRadioButton=window.findChild(QRadioButton,"rdoEasy")
        self.rdoMedium:QRadioButton=window.findChild(QRadioButton,"rdoMedium")
        self.rdoHard:QRadioButton=window.findChild(QRadioButton,"rdoHard")
        self.rdoVowelsEnabled:QRadioButton=window.findChild(QRadioButton,"rdoVowelsEnabled")
        self.rdoVowelsDisabled:QRadioButton=window.findChild(QRadioButton,"rdoVowelsDisabled")

    def _setup_image_label(self)->None:
        """
        Configures the image display label.

        Centers the image inside the label and disables automatic scaling,
        allowing manual control over aspect ratio and rendering behavior.
        """
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.lblImage.setScaledContents(False)

    def _assert_ui(self)->None:
        """
        Validates that all required UI widgets have been correctly retrieved.

        Checks whether any widget reference is None (due to a missing or incorrect
        objectName in the Qt Designer file) and raises a runtime error if validation fails.
        """
        items={"lblImage":self.lblImage,"lblWordPreview":self.lblWordPreview,"lblWord":self.lblWord,"txtAnswer":self.txtAnswer,"btnBack":self.btnBack,"btnNext":self.btnNext,"btnFolder":self.btnFolder,"btnReset":self.btnReset,"progressBar":self.progressBar,"rdoEasy":self.rdoEasy,"rdoMedium":self.rdoMedium,"rdoHard":self.rdoHard,"rdoVowelsEnabled":self.rdoVowelsEnabled,"rdoVowelsDisabled":self.rdoVowelsDisabled}
        missing=[name for name,w in items.items() if w is None]
        if missing:
            raise RuntimeError(f"Missing widgets in UI (wrong objectName): {missing}")

    def _wire_events(self)->None:
        """
        Connects UI signals to their corresponding handler methods.

        User interactions such as button clicks, text submission, and radio button
        toggles are linked to controller callbacks using Qt's signal-slot mechanism.
        """
        self.btnFolder.clicked.connect(self._on_folder_clicked)
        self.btnReset.clicked.connect(self._on_reset_clicked)
        self.btnNext.clicked.connect(self._on_next_clicked)
        self.btnBack.clicked.connect(self._on_back_clicked)
        self.txtAnswer.returnPressed.connect(self._on_submit_answer)
        self.rdoVowelsEnabled.toggled.connect(self._on_vowels_toggled)
        self.rdoVowelsDisabled.toggled.connect(self._on_vowels_toggled)
        self.rdoEasy.toggled.connect(self._on_difficulty_toggled)
        self.rdoMedium.toggled.connect(self._on_difficulty_toggled)
        self.rdoHard.toggled.connect(self._on_difficulty_toggled)

    def _start_from_folder(self,folder:str)->None:
        """
        Initializes a new game session starting from the selected folder.

        Stores the selected folder, enables difficulty selection, retrieves and
        shuffles image paths, and loads the dataset. If no valid images are found,
        a warning is shown and the application state is reset.
        """
        self.state.selectedFolder=folder
        self._set_difficulty_enabled(True)
        self._force_hard_default()
        paths=game_logic.get_image_paths(folder)
        if not paths:
            self._show_no_images_warning(folder)
            self._reset_state()
            return
        random.shuffle(paths)
        self._load_paths(paths)
        self.btnReset.setEnabled(True)

    def _on_folder_clicked(self)->None:
        """
        Handles the folder selection button click.

        Opens a directory selection dialog and starts a new session using the
        chosen folder if a valid path is provided.
        """
        folder=QFileDialog.getExistingDirectory(self.window,"Select image folder")
        if not folder:
            return
        self._start_from_folder(folder)

    def _on_reset_clicked(self)->None:
        """
        Handles the reset button click.

        Restarts the current session using the previously selected folder.
        If no folder is set, the reset action is disabled.
        """
        if not self.state.selectedFolder:
            self.btnReset.setEnabled(False)
            return
        self._start_from_folder(self.state.selectedFolder)

    def _load_paths(self,paths:list[str])->None:
        """
        Loads image paths into the application state and initializes game data.

        Sets the image list and current index, derives target words from file names,
        builds underscore patterns, reveal orders, and initial letter states, and
        updates the progress bar. Difficulty rules are applied before refreshing
        the current view.
        """
        self.state.imagePaths=paths
        self.state.currentIndex=0
        self.state.fullWords=[game_logic.sanitize_word_from_filename(p) for p in self.state.imagePaths]
        self.state.underscoreLines=[game_logic.build_underscore_line(w,self._vowels_enabled()) for w in self.state.fullWords]
        self.state.revealOrders=[game_logic.build_reveal_order(w) for w in self.state.fullWords]
        self.state.letterStates=[[" " if ch==" " else " " for ch in w] for w in self.state.fullWords]
        self.progressBar.setRange(0,len(self.state.imagePaths)-1)
        self.progressBar.setValue(self.state.currentIndex)
        self._apply_difficulty_to_all_unsolved_overwrite()
        self._refresh_current_view()

    def _refresh_current_view(self)->None:
        """
        Refreshes the entire user interface for the current item.

        Updates the puzzle labels, displays the current image, and adjusts
        navigation button states to reflect the current position.
        """
        self._refresh_puzzle_labels()
        self._show_current_image()
        self._update_navigation_buttons()

    def _on_next_clicked(self)->None:
        """
        Handles the next button click.

        Moves to the next image if available, updates the progress bar,
        and refreshes the current view.
        """
        if self.state.currentIndex<len(self.state.imagePaths)-1:
            self.state.currentIndex+=1
            self.progressBar.setValue(self.state.currentIndex)
            self._refresh_current_view()

    def _on_back_clicked(self)->None:
        """
        Handles the back button click.

        Moves to the previous image if possible, updates the progress bar,
        and refreshes the current view.
        """
        if self.state.currentIndex>0:
            self.state.currentIndex-=1
            self.progressBar.setValue(self.state.currentIndex)
            self._refresh_current_view()

    def _on_submit_answer(self)->None:
        """
        Handles user answer submission.

        Normalizes the input and compares it with the target word. If the guess is
        correct, the word is fully revealed and the view advances if applicable.
        If incorrect, a random unrevealed letter is revealed and the puzzle labels
        are updated accordingly.
        """
        if self.state.currentIndex<0 or self.state.currentIndex>=len(self.state.fullWords):
            self.txtAnswer.clear()
            return
        raw=self.txtAnswer.text()
        self.txtAnswer.clear()
        guess=game_logic.normalize_user_input(raw)
        if not guess:
            return
        word=self.state.fullWords[self.state.currentIndex]
        was_already_fully_revealed=self._is_solved(self.state.currentIndex)
        if guess==word:
            self.state.letterStates[self.state.currentIndex]=list(word)
            self._refresh_puzzle_labels()
            if (not was_already_fully_revealed) and self.state.currentIndex<len(self.state.imagePaths)-1:
                self._on_next_clicked()
            return
        changed=game_logic.reveal_one_random_letter(word,self.state.letterStates[self.state.currentIndex])
        if changed:
            self._refresh_puzzle_labels()
            if self._is_solved(self.state.currentIndex):
                return

    def _show_current_image(self)->None:
        """
        Displays the current image centered within the image label.

        Loads the image corresponding to the current index, scales it while
        preserving aspect ratio, and draws it onto a transparent canvas so
        that it appears centered inside the label.
        """
        if self.state.currentIndex<0 or self.state.currentIndex>=len(self.state.imagePaths):
            self.lblImage.clear()
            return
        pixmap=QPixmap(self.state.imagePaths[self.state.currentIndex])
        if pixmap.isNull():
            self.lblImage.clear()
            return
        target=self.lblImage.size()
        if target.width()<=0 or target.height()<=0:
            return
        scaled=pixmap.scaled(target,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        canvas=QPixmap(target)
        canvas.fill(Qt.transparent)
        painter=QPainter(canvas)
        x=(target.width()-scaled.width())//2
        y=(target.height()-scaled.height())//2
        painter.drawPixmap(x,y,scaled)
        painter.end()
        self.lblImage.setPixmap(canvas)

    def _update_navigation_buttons(self)->None:
        """
        Updates the enabled state of navigation buttons.

        Enables or disables the back, next, and reset buttons based on the
        current position and whether a folder has been selected.
        """
        self.btnBack.setEnabled(self.state.currentIndex>0)
        self.btnNext.setEnabled(self.state.currentIndex<len(self.state.imagePaths)-1)
        self.btnReset.setEnabled(bool(self.state.selectedFolder))

    def _reset_state(self)->None:
        """
        Resets the application to its initial demo state.

        Clears the current session data, disables difficulty selection, resets
        all UI elements to their default values, and shows the demo word preview.
        Navigation and reset controls are disabled.
        """
        self.state=AppState.empty()
        self._set_difficulty_enabled(False)
        self.lblImage.clear()
        self.lblWordPreview.setText(game_logic.spaced(list(self.demoWord)))
        self.lblWord.setText(game_logic.spaced(game_logic.build_underscore_line(self.demoWord,self._vowels_enabled())))
        self.txtAnswer.clear()
        self.progressBar.setRange(0,0)
        self.progressBar.setValue(0)
        self.btnBack.setEnabled(False)
        self.btnNext.setEnabled(False)
        self.btnReset.setEnabled(False)

    def _refresh_puzzle_labels(self)->None:
        """
        Updates the puzzle text labels for the current word.

        Refreshes the preview label showing revealed letters and the reference
        underscore pattern label based on the current game state.
        """
        if self.state.currentIndex<0 or self.state.currentIndex>=len(self.state.fullWords):
            return
        self.lblWordPreview.setText(game_logic.spaced(self.state.letterStates[self.state.currentIndex]))
        self.lblWord.setText(game_logic.spaced(self.state.underscoreLines[self.state.currentIndex]))

    def _vowels_enabled(self)->bool:
        """
        Checks whether the vowel hint option is enabled.

        Returns True if the vowel reveal radio button is selected, indicating
        that vowels should be shown in the puzzle pattern.
        """
        return self.rdoVowelsEnabled.isChecked()

    def _on_vowels_toggled(self)->None:
        """
        Handles changes to the vowel hint option.

        Rebuilds the underscore patterns for all words based on the current
        vowel setting and refreshes the puzzle labels. If no session is active,
        updates the demo preview instead.
        """
        if self.state.fullWords and self.state.currentIndex>=0:
            self.state.underscoreLines=[game_logic.build_underscore_line(w,self._vowels_enabled()) for w in self.state.fullWords]
            self._refresh_puzzle_labels()
            return
        self.lblWordPreview.setText(game_logic.spaced(list(self.demoWord)))
        self.lblWord.setText(game_logic.spaced(game_logic.build_underscore_line(self.demoWord,self._vowels_enabled())))

    def _difficulty_percent(self)->float:
        """
        Returns the letter reveal percentage associated with the selected difficulty.

        Easy reveals a higher fraction of letters, medium reveals fewer, and hard
        reveals none.
        """
        if self.rdoEasy.isChecked():
            return 0.60
        if self.rdoMedium.isChecked():
            return 0.30
        return 0.0

    def _set_difficulty_enabled(self,enabled:bool)->None:
        """
        Enables or disables the difficulty selection controls.

        Activates or deactivates the difficulty radio buttons based on the
        current application state.
        """
        self.rdoEasy.setEnabled(enabled)
        self.rdoMedium.setEnabled(enabled)
        self.rdoHard.setEnabled(enabled)

    def _force_hard_default(self)->None:
        """
        Forces the difficulty selection to hard mode.

        Sets the hard difficulty radio button as the default active option.
        """
        self.rdoHard.setChecked(True)

    def _on_difficulty_toggled(self)->None:
        """
        Handles changes to the selected difficulty level.

        Applies the new difficulty rules to all unsolved words and refreshes
        the puzzle labels accordingly.
        """
        if not self.state.fullWords or self.state.currentIndex<0:
            return
        self._apply_difficulty_to_all_unsolved_overwrite()
        self._refresh_puzzle_labels()

    def _is_solved(self,index:int)->bool:
        """
        Checks whether the word at the given index has been fully solved.

        Delegates the check to the game_logic utility by comparing the target word
        with its current revealed letter state.
        """
        return game_logic.is_solved(self.state.fullWords[index],self.state.letterStates[index])

    def _apply_difficulty_to_all_unsolved_overwrite(self)->None:
        """
        Applies the current difficulty settings to all unsolved words.

        Delegates the operation to the game_logic module, overwriting the letter
        states based on the selected difficulty percentage.
        """
        game_logic.apply_difficulty_to_all_unsolved_overwrite(self.state.fullWords,self.state.revealOrders,self.state.letterStates,self._difficulty_percent())

    def _show_no_images_warning(self,folderPath:str)->None:
        """
        Displays a warning dialog when no supported images are found.

        Shows a message box informing the user that the selected folder does not
        contain valid image files and lists the supported formats.
        """
        msg=QMessageBox(self.window)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(CONFIG.noImagesTitle)
        msg.setWindowIcon(self.window.windowIcon())
        msg.setText(CONFIG.noImagesText+"\n\n"+f"Folder:\n{folderPath}\n\n"+CONFIG.noImagesFormats)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
