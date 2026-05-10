import random
import re
from pathlib import Path

def get_image_paths(folder:str)->list[str]:
    """
    Returns the paths of all valid image files contained in the given folder.

    Parameters:
    - folder (str): directory to scan

    Returns:
    - list[str]: list of image file paths
    """
    valid_extensions={".png",".jpg",".jpeg",".bmp",".gif",".webp"}
    return [str(p) for p in Path(folder).iterdir() if p.is_file() and p.suffix.lower() in valid_extensions]

def sanitize_word_from_filename(path:str)->str:
    """
    Extracts and normalizes a word from an image file name.

    The file extension is removed, the name is converted to lowercase,
    non-letter characters are discarded, and extra spaces are normalized.

    Parameters:
    - path (str): file path of the image

    Returns:
    - str: sanitized word derived from the file name
    """
    name=Path(path).name
    if "." in name:
        name=name.split(".",1)[0]
    name=name.lower()
    name=re.sub(r"[^a-zàèéìòù\s]","",name)
    name=re.sub(r"\s+"," ",name).strip()
    return name

def normalize_user_input(text:str)->str:
    """
    Normalizes user input for comparison with the target word.

    The input is converted to lowercase, non-letter characters are removed,
    and multiple spaces are collapsed into a single space.

    Parameters:
    - text (str): raw user input

    Returns:
    - str: normalized input string
    """
    text=text.lower().strip()
    text=re.sub(r"[^a-zàèéìòù\s]","",text)
    text=re.sub(r"\s+"," ",text).strip()
    return text

def is_vowel(ch:str)->bool:
    """
    Checks whether a character is a vowel.

    Both standard and accented vowels are considered.

    Parameters:
    - ch (str): character to be checked

    Returns:
    - bool: True if the character is a vowel, False otherwise
    """
    return ch in {"a","e","i","o","u","à","è","é","ì","ò","ù"}

def build_underscore_line(word:str,vowels_on:bool)->list[str]:
    """
    Builds the reference pattern line for a target word.

    Spaces are preserved, vowels can be revealed as '+' when enabled,
    and all other characters are represented as '-'.

    Parameters:
    - word (str): target word
    - vowels_on (bool): whether vowels should be revealed

    Returns:
    - list[str]: list representing the underscore pattern of the word
    """
    out=[]
    for ch in word:
        if ch==" ":
            out.append(" ")
        elif vowels_on and is_vowel(ch):
            out.append("+")
        else:
            out.append("-")
    return out

def spaced(chars:list[str])->str:
    """
    Converts a list of characters into a space-separated string.

    Parameters:
    - chars (list[str]): list of characters

    Returns:
    - str: characters joined with spaces
    """
    return " ".join(chars)

def build_reveal_order(word:str)->list[int]:
    """
    Generates a randomized reveal order for the characters of a word.

    Only non-space character positions are included, and their indices
    are shuffled to define a random reveal sequence.

    Parameters:
    - word (str): target word

    Returns:
    - list[int]: shuffled list of character indices
    """
    indices=[i for i,ch in enumerate(word) if ch!=" "]
    random.shuffle(indices)
    return indices

def is_solved(word:str,state:list[str])->bool:
    """
    Checks whether a word has been completely solved.

    All non-space characters of the word must match the corresponding
    positions in the current state.

    Parameters:
    - word (str): target word
    - state (list[str]): current revealed character state

    Returns:
    - bool: True if the word is fully solved, False otherwise
    """
    for i,ch in enumerate(word):
        if ch==" ":
            continue
        if state[i]!=ch:
            return False
    return True

def reveal_one_random_letter(word:str,state:list[str])->bool:
    """
    Reveals one random unrevealed character of the target word.

    A character is selected only if it is not a space and has not yet
    been revealed in the current state. The state is modified in place.

    Parameters:
    - word (str): target word
    - state (list[str]): current revealed character state

    Returns:
    - bool: True if a character was revealed, False if no candidates exist
    """
    candidates=[i for i,ch in enumerate(word) if ch!=" " and state[i]!=ch]
    if not candidates:
        return False
    i=random.choice(candidates)
    state[i]=word[i]
    return True

def apply_difficulty_to_all_unsolved_overwrite(fullWords:list[str],revealOrders:list[list[int]],letterStates:list[list[str]],percent:float)->None:
    """
    Applies a difficulty level to all unsolved words by pre-revealing letters.

    For each unsolved word, a new letter state is built from scratch and a
    percentage of characters is revealed according to the predefined reveal
    order. Already solved words are left unchanged. The letter states are
    overwritten in place.

    Parameters:
    - fullWords (list[str]): list of target words
    - revealOrders (list[list[int]]): randomized reveal orders for each word
    - letterStates (list[list[str]]): current letter states to be overwritten
    - percent (float): fraction of characters to reveal (0.0–1.0)

    Returns:
    - None
    """
    for i,w in enumerate(fullWords):
        if is_solved(w,letterStates[i]):
            continue
        order=revealOrders[i]
        n=int(round(len(order)*percent))
        n=max(0,min(n,len(order)))
        newState=[" " if ch==" " else " " for ch in w]
        for pos in order[:n]:
            newState[pos]=w[pos]
        letterStates[i]=newState
