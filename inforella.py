import os
import argparse
import re
import _colorize as color
import _pep_check as pep
import configparser


# аргументы командой строки
cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")
args = cli.parse_args()

# работа с конфигом
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

count_lines_code, count_def_code, count_comments_code = 0, 0, 0
# дерево файлов
tree = os.walk(args.dir)

all_files = []

# Цвета
GREEN = color.Back.GREEN
RED = color.Back.RED
CYAN = color.Back.CYAN


def is_python_file(name_file: str) -> bool:
    """
    Проверяет, имеет ли файл расширение .py
    :param name_file: имя файла
    :return: Имеет ли файл расширение .py
    """
    return '.py' == name_file[-3::]


def count_word_file(name_file: str, word: str) -> int:
    """
    Возвращает количество определённых слов в файле
    :param name_file: Имя файла
    :param word: Слово по поиску в файле
    :return: Количество слов
    """
    count_words = 0
    with open(name_file, encoding='utf-8') as file_func:
        for line in file_func:
            count_words += len(re.findall(word, line))

    return count_words

def is_char_in_quotes(symbol: str,line: str) -> bool:
    """
    Функция возвращает bool значения, находится ли char в кавычках
    :param symbol: символ
    :param line: строка
    :return: True или False
    """
    try:
        position_symbol = line.index(symbol)
        for symbol in range(position_symbol,-1,-1):
            if line[symbol] == "'" or line[symbol] == '"':
                return False
        return True

    except ValueError:
        return False


try:
    for files in tree:
        for file in files[2]:
            # если файл имеет расширение .py
            if is_python_file(file):
                path_file = files[0] + '/' + file
                # считаем кол-во строк в файле
                count_lines_code += sum(1 for line in open(files[0] + '/' + file, encoding='utf-8'))
                # считаем количество функций в файле
                count_def_code += count_word_file(path_file, 'def')
                # считаем количество количествомментарий в файле
                count_comments_code += count_word_file(path_file, '#') + int(count_word_file(path_file, '"""') / 2)

                all_files.append(path_file)
except FileNotFoundError:
    print('Не удалось найти директорию')

except Exception as e:
    print(f'Упс...\nЧто-то пошло не так\n - {e} -')


def pep8_test(all_file):
    pep_warnings = ''
    for file in all_file:
        pep_warnings += f'{file.split("/")[-1]} - {"Не отсуплено 2 строки после импортов"}\n' \
                        if not pep.pep_import_check(file) else ''
        pep_warnings += pep.pep_line_length_check(file, int(config['Norms']['length_line_limit']))
        pep_warnings += pep.comments_correction(file)
        pep_warnings += pep.commas_style_check(file)

    if pep_warnings:
        color.line_design('#')
        print(color.color_text(CYAN, 'PEP 8 WARNING'))
        print(pep_warnings)


def tree_files(all_files: list):
    """
    :param all_files: Все файлы проекта
    :return: None
    """
    print('Все файлы проекта :')
    for file in all_files:
        print(f'  - {file.split("/")[-1]}')
    print('')


def testing_variable_length(all_files):
    """
    :param all_files: все файлы
    Функция возвращает словарь, где ключи - длина строк, а значения - количество подобных строк в коде
    """
    all_variable_length = {}

    for file in all_files:
        with open(file, encoding='utf-8') as file:
            for line in file.readlines():
                if re.findall(r'\S+ = \S+', line) and not re.findall(r'\S+ \+= \S+',line) and not re.findall(',',line.split('=')[0]) and is_char_in_quotes('=',line):
                    name_variable = line.split('=')[0].rstrip(' ').lstrip(' ').split('.')[-1]
                    if not len(name_variable) in all_variable_length:
                        all_variable_length[len(name_variable)] = 1
                    else:
                        all_variable_length[len(name_variable)] += 1

    return all_variable_length


def validate():
    """ Вывод и валидация результатов """
    tree_files(all_files)

    print('Длина названий перменных\nФормат: длина строки -> количество подобных строк\n')
    for key, value in testing_variable_length(all_files).items():
        print(f'{key} символов -> в {value} строках')
    print('')

    function_norm = int(count_lines_code / int(config["Norms"]["function_norm"]))
    comments_norm = int(count_lines_code / int(config["Norms"]["comments_norm"]))

    print(f'Количество строк кода - {count_lines_code}\n')
    print(f'Количество файлов в проекте - {len(all_files)}\n')
    print(f'Количество функций в проекте - {count_def_code}\n')

    print(color.color_text(GREEN, 'Функций достаточно!')) if count_def_code > function_norm else \
    print(color.color_text(RED, 'Количество функций, меньше чем ожидалось!'))
    print(f'Количество комментарий в проекте - {count_comments_code}\n')

    print(color.color_text(GREEN, 'Комментариев много,респект!')) if count_comments_code > comments_norm else \
    print(color.color_text(RED, 'Маловато комментариев, никто же не поймёт ничего...'))


if __name__ == '__main__':
    validate()
    pep8_test(all_files)
