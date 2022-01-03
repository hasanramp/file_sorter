import click
from termcolor import colored
from files_sorter import SortFiles
import time
import os
import platform

start_time = time.time()

file_dir = os.path.abspath(__file__)
if platform.system() == 'Linux':
	parent_dir_list = file_dir.split('/')
else:
	parent_dir_list = file_dir.split('\\')
parent_dir_list.remove('')
parent_dir_list.remove(parent_dir_list[-1])

if platform.system() == 'Linux':
	parent_dir = '/'.join(parent_dir_list)
	parent_dir = '/' + parent_dir

os.chdir(parent_dir)

def sort_files(files_sorter):
    files_sorter.get_pattern_matches()
    colored_number_of_files = colored(str(files_sorter.number_of_files_moved), 'cyan')
    print(f'\n\nnumber of files moved: {colored_number_of_files}')
    added_folders_dict = files_sorter.to_move_dirs_dict
    text_colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    index = 0
    for key in added_folders_dict.keys():
        n_of_files = added_folders_dict[key]
        if n_of_files != 0:
            text = colored(f'files added in {key}: {n_of_files}', text_colors[index])
            print(text)
        index += 1

@click.group()
def file_sorter():
    pass

@file_sorter.command()
@click.option('--def_dir', '--default_dir', '--d', type=str, default=None)
def sort(def_dir):
    if def_dir != None:
        parent_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(parent_dir, def_dir)
        files_sorter = SortFiles(base_dir=base_dir)
    else:
        files_sorter = SortFiles()
    
    sort_files(files_sorter)

@file_sorter.command()
@click.option('--def_dir', '--default_dir', '--d', type=str, default=None)
def detect(def_dir):
    if def_dir != None:
        parent_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(parent_dir, def_dir)
        files_sorter = SortFiles(base_dir=base_dir)
    else:
        files_sorter = SortFiles()
    matched_files = files_sorter.detect_to_move_files()
    if matched_files == []:
        print(colored('no files to sort', 'cyan'))
    else:
        print('\n')
        for file in matched_files:
            print(file)
        print('\n')

if __name__ == '__main__':
    file_sorter()

time_taken = str(time.time() - start_time)
time_taken = colored(time_taken, 'magenta')
print(f'finished in {time_taken} seconds')