import os
import argparse
import re
import _colorize as color
import _pep_check as pep


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")

args = cli.parse_args()
count_lines_code, count_def_code, count_comments_code = 0, 0, 0

tree = os.walk(args.dir) # дерево файлов

all_files = []

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
                count_comments_code += count_word_file(path_file, '#') + count_word_file(path_file, '"""')

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
        pep_warnings += pep.pep_line_length_check(file)
        pep_warnings += pep.comments_correction(file)

    if pep_warnings:
        color.line_design('#')
        print(color.color_text(CYAN, 'PEP 8 WARNING'))
        print(pep_warnings)


def tree_files(all_files: list):
    """
    :param files_:
    :return:
    """
    print('Все файлы проекта :')
    for file in all_files:
        print(f'  - {file.split("/")[-1]}')
    print('')


def validate():
    """ Вывод и валидация результатов """
    tree_files(all_files)
    function_norm = int(count_lines_code / 30)
    comments_norm = int(count_lines_code / 10)

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
