# make_example_env.py
# a script that will take a supplied environment file and make an example
# file for it in the same directory
# PaddyAlton -- 2018-09-11

import sys
import glob

def create_example(file_name):
    """create_example generates an example counterpart for a .env file"""

    with open(file_name) as file_object:
        text = file_object.readlines()

    sanitised_text = [line.split('=')[0]+'= \n' for line in text]

    new_file_name = f"{file_name}.example"

    with open(new_file_name, mode="w+") as file_object:
        _ = file_object.writelines(sanitised_text)

if __name__ == "__main__":

    path_to_config = sys.argv[1]

    file_list = [
        f for f in sorted(glob.glob(path_to_config+'/.*'))
        if not f.endswith('.gitkeep')
    ]

    for file_name in file_list:
        create_example(file_name)
