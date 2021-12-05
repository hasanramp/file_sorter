import time
from files_sorter import SortFiles
import os
from termcolor import colored
import argparse

start_time = time.time()



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


sort_parser = argparse.ArgumentParser()
sort_parser.add_argument("sort", help="sorts the files of the default directory")
sort_parser.add_argument("--def_dir")

sort_args = sort_parser.parse_args()
if sort_args.sort == 'sort':
    if sort_args.def_dir != None:
        parent_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(parent_dir, sort_args.def_dir)
        files_sorter = SortFiles(base_dir=base_dir)
    else:
        files_sorter = SortFiles()
    sort_files(files_sorter)

elif sort_args.sort == 'detect':
    if sort_args.def_dir != None:
        parent_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(parent_dir, sort_args.def_dir)
        files_sorter = SortFiles(base_dir=base_dir)
    else:
        files_sorter = SortFiles()
    matched_files = files_sorter.detect_to_move_files()
    if matched_files == []:
        print('no files to sort')
    else:
        print('\n')
        for file in matched_files:
            print(file)
        print('\n')

time_taken = time.time() - start_time
time_taken = colored(str(time_taken), 'magenta')
print(f'finished in {time_taken} seconds')