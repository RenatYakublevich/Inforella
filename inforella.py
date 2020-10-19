import os 
import argparse


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")


def is_cache_file(name_file : str) -> bool:
	""" Проверяет, является ли файл кешом Python интерпритатора """
	return '.pyc' == name_file[-4::]

try:
	args = cli.parse_args()
	count_lines_code, count_def_code, count_files = 0, 0, 0
	tree = os.walk(args.dir)
	for files in tree:
		for file in files[2]:
			try:
				if not is_cache_file(file):
					count_files += 1
				count_lines_code += sum(1 for line in open(files[0] + '/' + file, encoding='utf-8'))
			except UnicodeDecodeError:
				pass

	print(f'Количество строк кода - {count_lines_code}')
	print(f'Количество файлов в проекте - {count_files}')

except FileNotFoundError:
	print('Не удалось найти директорию')
