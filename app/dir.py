import os
from pprint import pprint


def diff_dir_with_filelist(directory, filepath):
    new_files = os.listdir(directory)
    with open(filepath, 'r') as text_file:
        old_list = text_file.readlines()

    old_files = set(item.rstrip() for item in old_list)
    return [x for x in new_files if x not in old_files]


results = diff_dir_with_filelist("_Photos/", "./bot_photo_202311131157.txt")
pprint(results)
