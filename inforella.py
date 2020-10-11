import os 
import argparse


cli = argparse.ArgumentParser(description='Inforella')
cli.add_argument("--dir", default='.', type=str, help="Директория для сканирования")

args = cli.parse_args()

all_file = [file for file in os.listdir(args.dir)]
count_files = len(all_file)

count_lines_code = 0

tree = os.walk(args.dir)

for files in tree:
	for file in files[2]:
		try:
			count_lines_code += sum(1 for line in open(files[0] + '/' + file,encoding='utf-8'))
		except UnicodeDecodeError:
			pass

		
	

print(f'Количество строк кода - {count_lines_code}')






