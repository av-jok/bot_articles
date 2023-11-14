import os
import re
from pprint import pprint


def diff_dir_with_filelist(directory, filepath):
    new_files = os.listdir(directory)
    with open(filepath, 'r') as text_file:
        old_list = text_file.readlines()

    old_files = set(item.rstrip() for item in old_list)
    return [x for x in new_files if x not in old_files]


results = diff_dir_with_filelist("_Photos/", "./bot_photo.csv")
out = []

for i in results:
    b = re.match('^\\d{5}', i)
    out.append({'id':b[0], 'file':i})
    print(f"{b[0]};{i}")

# pprint(out)


