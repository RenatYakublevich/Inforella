import os 
import argparse
import re


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")

args = cli.parse_args()
count_lines_code, count_def_code, count_files = 0, 0, 0
tree = os.walk(args.dir)


def is_cache_file(name_file: str) -> bool:
	""" Проверяет, является ли файл кешом Python интерпритатора """
	return '.pyc' == name_file[-4::]


def count_function_file(name_file: str) -> int:
	count_def = 0
	with open(name_file, encoding='utf-8') as file_func:
		for line in file_func:
			count_def += len(re.findall(r'def', line))

	return count_def


try:
	for files in tree:
		for file in files[2]:
			try:
				# если файл не кеш
				if not is_cache_file(file):
					count_files += 1
				# считаем кол-во строк в файле
				count_lines_code += sum(1 for line in open(files[0] + '/' + file, encoding='utf-8'))
				count_def_code += count_function_file(files[0] + '/' + file)
			except UnicodeDecodeError:
				pass
	print(f'Количество строк кода - {count_lines_code}\n')
	print(f'Количество файлов в проекте - {count_files}\n')
	print(f'Количество функций в проекте - {count_def_code}\n')

except FileNotFoundError:
	print('Не удалось найти директорию')
except Exception:
	print('Упс...\nЧто-то пошло не так')
