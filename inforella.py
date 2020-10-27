import os
import argparse
import re
import _colorize as color
import _pep_check as pep


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")

args = cli.parse_args()
count_lines_code, count_def_code, count_files, count_comments_code = 0, 0, 0, 0
# дерево файлов
tree = os.walk(args.dir)
pep_warning = ''

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
                count_files += 1
                # считаем кол-во строк в файле
                count_lines_code += sum(1 for line in open(files[0] + '/' + file, encoding='utf-8'))
                # считаем количество функций в файле
                count_def_code += count_word_file(path_file, 'def')
                # считаем количество комментарий в файле
                count_comments_code += count_word_file(path_file, '#') + \
                count_word_file(path_file, '"""')

                # тесты на PEP 8
                # pep_warning += pep.pep_test_machine(pep.pep_import_check(path_file), 'Всё гуд!', 'Всё хуйня давай по новой'))



except FileNotFoundError:
    print('Не удалось найти директорию')

except Exception:
    print('Упс...\nЧто-то пошло не так')


def if_machine(statement1, statement2, text, else_text):
    """
    :param statement1: первое условие
    :param statement2: второе условие
    :param text: текст, если первое условие верное
    :param else_text: альтернативный текст
    :return: None
    """
    if statement1 > statement2:
        print(text)
    else:
        print(else_text)


def validate():
    """ Вывод и валидация результатов """
    GREEN = color.Back.GREEN
    RED = color.Back.RED
    CYAN = color.Back.CYAN

    function_norm = int(count_lines_code / 30)
    comments_norm = int(count_lines_code / 10)

    print(f'Количество строк кода - {count_lines_code}\n')
    print(f'Количество файлов в проекте - {count_files}\n')
    print(f'Количество функций в проекте - {count_def_code}\n')
    if_machine(statement1=count_def_code, statement2=function_norm,
               text=color.color_text(GREEN, 'Функций достаточно!'),
               else_text=color.color_text(RED, 'Количество функций, меньше чем ожидалось!'))
    print(f'Количество комментарий в проекте - {count_comments_code}\n')
    if_machine(statement1=count_comments_code, statement2=comments_norm,
               text=color.color_text(GREEN, 'Комментариев много,респект!'),
               else_text=color.color_text(RED, 'Маловато комментариев, никто же не поймёт ничего...'))
    color.line_design('#')
    print(color.color_text(CYAN, 'PEP 8 ANALYSIS'))

    
validate()
