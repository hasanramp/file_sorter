import os
import re
import shutil
from datetime import date
import json
import time

class SortFiles:
    def __init__(self, to_track_dir=None, sort_in_default_dir=True):
        self.number_of_files_moved = 0
        patterns, default_dir, end_dirs = self.get_config()
        self.default_dir = default_dir
        self. patterns = patterns
        if to_track_dir is not None:
            self.to_track_dir = to_track_dir
        else:
            parent_dir = os.path.dirname(os.getcwd())
            self.to_track_dir = os.path.join(parent_dir, default_dir)
        self.sort_in_default_dir = sort_in_default_dir
        if sort_in_default_dir is True:
            to_sort_dir = default_dir
            self.to_sort_dir = os.path.join(os.path.dirname(os.getcwd()), default_dir)
        elif type(sort_in_default_dir) == str:
            to_sort_dir = sort_in_default_dir
            self.to_sort_dir = os.path.join(os.path.dirname(os.getcwd()), to_sort_dir)
        elif sort_in_default_dir is False:
            to_sort_dir = self.to_track_dir
            self.to_sort_dir = os.path.join(os.path.dirname(os.getcwd()), to_sort_dir)
        else:
            print('Invalid type for to_sort_dir')
            exit()
        # self.to_sort_dir = to_sort_dir
        
        self.end_dirs = end_dirs
        arr = []
        for x in self.end_dirs:
            arr.append(0)

        self.to_move_dirs_dict = dict(zip(self.end_dirs, arr))

    def move_file(self, pattern, filename, end_dir):
        to_track_dir = self.to_track_dir
        print(f'file for {end_dir} detected....')
        print(f'moving file to {end_dir}...')
        final_destination = ''
        original_dest = os.path.join(to_track_dir, filename)
        # if self.sort_in_default_dir is True:
        #     self.to_sort_dir = os.path.join(os.path.dirname(os.getcwd()), self.default_dir)
        final_dir = os.path.join(self.to_sort_dir, end_dir)
        # print(final_dir)
        # exit()
        final_dir_exists = os.path.isdir(final_dir)
        if final_dir_exists is False:
            os.mkdir(final_dir)
        if pattern == 'tt.pdf':
            final_destination = os.path.join(self.to_sort_dir, end_dir, date.today().strftime('%d-%m-%Y') + f'_{filename}')
            shutil.move(original_dest,
                        final_destination)

        elif pattern == '2021-23.pdf':
            final_destination = os.path.join(self.to_sort_dir, end_dir, date.today().strftime('%d-%m-%Y') + f'_{filename}')
            shutil.move(original_dest, final_destination)

        elif pattern == '.appimage' or '.AppImage' or '.deb':
            final_destination = os.path.join(self.to_sort_dir, end_dir, f'{filename}')
            try:
                shutil.move(original_dest, final_destination)
            except FileNotFoundError:
                print('\n\nthere was some error while moving file: ' + filename)
                print('were there files with nested extensions?')
                print('This may occur because of it. File was probably sorted')
                time.sleep(3)
        else:
            print('reached here')
            exit()
            final_destination = os.path.join(self.to_sort_dir, end_dir, f'{filename}')
            shutil.move(original_dest, final_destination)

        print(f'file moved to {end_dir} !')
        end_dir = end_dir.replace('/', '')
        self.to_move_dirs_dict[end_dir] += 1

    def get_pattern_matches(self):
        parent_dir = os.path.dirname(os.getcwd())
        to_track_dir = os.path.join(parent_dir, self.to_track_dir)
        directories = os.listdir(to_track_dir)
        for src_path in directories:
            index = 0
            for pattern in self.patterns:
                start_str, end_str = pattern
                if start_str is not None:
                    matches = re.search(f'^{start_str}.*{end_str}$', src_path)
                    if matches:

                        end_dir = self.end_dirs[index] + '/'
                        self.move_file(end_str, src_path, end_dir)
                        self.number_of_files_moved += 1
                else:
                    matches = re.search(f' *{end_str}$', src_path)
                    if matches:
                        print('reached here')
                        try:
                            end_dir = self.end_dirs[index] + '/'
                        except IndexError:
                            from termcolor import colored
                            print(colored(f'folder name was not specified for pattern {end_str}', 'red'))
                            exit()
                        self.move_file(end_str, src_path, end_dir)
                        self.number_of_files_moved += 1
                index += 1

    def detect_to_move_files(self):
        directories = os.listdir(self.to_track_dir)
        file_matches = []
        for src_path in directories:
            index = 0
            for pattern in self.patterns:
                start_str, end_str = pattern
                if start_str is not None:
                    matches = re.search(f'^{start_str}.*{end_str}$', src_path)
                    if matches:
                        file_matches.append(src_path)
                else:
                    matches = re.search(f' *{end_str}$', src_path)
                    if matches:
                        file_matches.append(src_path)
                index += 1
        return file_matches

    def get_config(self):
        config_file = open('config.json', 'r')
        config_json = json.load(config_file)
        return config_json['patterns'], config_json['default_dir'], config_json['end_dirs']

#, "setups"