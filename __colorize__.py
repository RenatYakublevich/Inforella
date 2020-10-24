from colorama import Fore,Style

GREEN_BACKGROUND = '\u001b[42;1m'
RED = '\u001b[1m\u001b[31m'


def color_text(color : str, text : str):
    return color + text + '\033[39m'
