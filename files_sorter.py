import os
import re
import shutil
from datetime import date
import json


class SortFiles:
    def __init__(self, base_dir=None):
        self.number_of_files_moved = 0
        patterns, default_dir, end_dirs = self.get_config()
        self. patterns = patterns
        if base_dir != None:
            self.base_dir = base_dir
        else:
            parent_dir = os.path.dirname(os.getcwd())
            self.base_dir = os.path.join(parent_dir, default_dir)
        self.end_dirs = end_dirs
        arr = []
        for x in self.end_dirs:
            arr.append(0)

        self.to_move_dirs_dict = dict(zip(self.end_dirs, arr))

    def move_file(self, pattern, filename, end_dir):
        base_dir = self.base_dir
        print(f'file for {end_dir} detected....')
        print(f'moving file to {end_dir}...')
        final_destination = ''
        original_dest = os.path.join(base_dir, filename)
        final_dir = os.path.join(base_dir, end_dir)
        final_dir_exists = os.path.isdir(final_dir)
        if final_dir_exists is False:
            os.mkdir(final_dir)
        if pattern == 'tt.pdf':
            final_destination = os.path.join(base_dir, end_dir, date.today().strftime('%d-%m-%Y') + f'_{filename}')
            shutil.move(original_dest,
                        final_destination)

        elif pattern == '2021-23.pdf':
            final_destination = os.path.join(base_dir, end_dir, date.today().strftime('%d-%m-%Y') + f'_{filename}')
            shutil.move(original_dest, final_destination)

        elif pattern == '.appimage' or '.AppImage' or '.deb':
            final_destination = os.path.join(base_dir, end_dir, f'{filename}')
            shutil.move(original_dest, final_destination)
        else:
            final_destination = os.path.join(base_dir, end_dir, f'{filename}')
            shutil.move(original_dest, final_destination)
            
        print(f'file moved to {end_dir} !')
        end_dir = end_dir.replace('/', '')
        self.to_move_dirs_dict[end_dir] += 1

    def get_pattern_matches(self):
        parent_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(parent_dir, self.base_dir)
        directories = os.listdir(base_dir)
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
                        end_dir = self.end_dirs[index] + '/'
                        self.move_file(end_str, src_path, end_dir)
                        self.number_of_files_moved += 1
                index += 1

    def detect_to_move_files(self):
        directories = os.listdir(self.base_dir)
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

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.getcwd())
    base_dir = os.path.join(parent_dir, 'Downloads')
    files_sorter = SortFiles(base_dir)
    directories = os.listdir(base_dir)
    matches = files_sorter.detect_to_move_files(directories)
    print(matches)