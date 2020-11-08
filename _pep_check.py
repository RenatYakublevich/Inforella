def pep_test_machine(statement, text, path_file):
    if not statement:
        return f'{path_file.split("/")[-1]} - {text}\n'
    return ''


def line_is_import(string: str):
    """
    :param string: строка кода
    :return: Является ли лайн импортом модуля
    """
    if not string.startswith('import') and not string.startswith('from'):
        return True


def pep_import_check(path_file: str):
    """
    :param path_file: код на проверку
    :return: Имеются ли отступы после импортов
    """
    try:
        with open(path_file, encoding='utf-8') as file:
            lines = file.readlines()
        if line_is_import(lines[0]):
            return True
        for line in range(0, len(lines)):
            if not line_is_import(lines[line]) and lines[line + 1] + lines[line + 2] == '\n\n':
                return True

        return False
    except IndexError:
        pass


def pep_line_length_check(path_file: str):
    with open(path_file, encoding='utf-8') as file:
        lines = file.readlines()
    length_warnings = ''
    count_lines = 0
    for line in lines:
        if len(line) > 120:
            length_warnings += f'{path_file.split("/")[-1]} - строка {count_lines + 1} ' \
                    'превышает предел длины строки(120 символов)\n'
        count_lines += 1
    if length_warnings:
        return length_warnings
    return ''
