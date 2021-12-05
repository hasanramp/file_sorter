# file_sorter
A one time file sorting application for linux. (I think it should work on windows as well)

## How to use
open config.json file
enter the name of the default directory you want to clean (the path is relative)
the patterns is an array of arrays. The first element of the inner array contains what the file name should start with. The second element contains what the file name should end with. The first element can be kept null. I know it's a dumb way to search for matches but it currently works for me. If you have a much more sophisticated method of searching, pull requests are more than welcome.

You can use the --def_dir flag to temporarily use another directory than the one in confi.json. this directory path should also be relative and should be present in parent directory of the directory in which these files are.
## Installation
clone repo and run main.py file

## Note
By default the Downloads directory is chosen. And it assumes the directory you are going to choose has a directory called AppImages and deb_files. You can change that in config.json

