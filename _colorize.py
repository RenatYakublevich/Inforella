from colorama import Fore, Style, init, Back


init()


def color_text(color: str, text: str):
    return color + text + Style.RESET_ALL + '\n'


def line_design(char: str):
    print(f'{char} ' * 20)

