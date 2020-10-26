import os 
import argparse
import re
import __colorize__ as color


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")

args = cli.parse_args()
count_lines_code, count_def_code, count_files, count_comments_code = 0, 0, 0, 0
# дерево файлов
tree = os.walk(args.dir)


def is_cache_file(name_file: str) -> bool:
    """
    Проверяет, является ли файл кешом Python интерпритатора
    :param name_file: имя файла
    :return: Имеет ли файл расширение .pyc
    """
    return '.pyc' == name_file[-4::]


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
            try:
                # если файл не кеш
                if not is_cache_file(file):
                    count_files += 1
                # считаем кол-во строк в файле
                count_lines_code += sum(1 for line in open(files[0] + '/' + file, encoding='utf-8'))
                # считаем количество функций в файле
                count_def_code += count_word_file(files[0] + '/' + file, 'def')
                # считаем количество комментарий в файле
                count_comments_code += count_word_file(files[0] + '/' + file, '#')
            except UnicodeDecodeError:
                pass


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
    function_norm = count_lines_code / 41
    comments_norm = count_lines_code / 15

    print(f'Количество строк кода - {count_lines_code}\n')
    print(f'Количество файлов в проекте - {count_files}\n')
    print(f'Количество функций в проекте - {count_def_code}\n')
    if_machine(statement1=count_def_code, statement2=function_norm,
               text=color.color_text(color.Back.GREEN, 'Функций достаточно!'),
               else_text=color.color_text(color.Back.RED, 'Количество функций, меньше чем ожидалось!'))
    print(f'Количество комментарий в проекте - {count_comments_code}')






validate()
