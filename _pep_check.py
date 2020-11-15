def line_is_import(string: str):
    """
    :param string: строка кода
    :return: Является ли лайн импортом модуля
    """
    if not string.startswith('import') and not string.startswith('from'):
        return True


def pep_import_check(path_file: str):
    """
    :param path_file: путь к файлу
    :return: Имеются ли отступы после импортов
    """
    with open(path_file, encoding='utf-8') as file:
        lines = file.readlines()
    if line_is_import(lines[0]):
        return True
    for line in range(0, len(lines) - 1):
        if not line_is_import(lines[line]) and lines[line + 1] + lines[line + 2] == '\n\n':
            return True

    return False


def pep_line_length_check(path_file: str):
    """
    :param path_file: путь к файлу
    :return: количество строк, которые превышают длину в 120 символов
    """
    with open(path_file, encoding='utf-8') as file:
        lines = file.readlines()
    length_warnings = ''
    count_lines = 0
    for line in lines:
        if len(line) > 120:
            length_warnings += f'{path_file.split("/")[-1]} - строка {count_lines + 1} ' \
                    'превышает предел длины строки(120 символов)\n'
        count_lines += 1
    return length_warnings


def comments_correction():
    pass
