# this script takes colab-env and copies its contents to a target directory
import os
import sys
import glob

from subprocess import run as shell

def spawn_new_standard_repo(target_name, subdir_name):
    """ spawn_new_standard_repo """
    shell(f"cp -r colab-env {target_name}", shell=True)
    shell(f"cp -r colab-env/.* {target_name}", shell=True)
    shell(f"mv {target_name}/colab_env {target_name}/{subdir_name}", shell=True)
    shell(
        f"mv {target_name}/k8s/live/colab-env.cron.yaml {target_name}/k8s/live/{target_name}.cron.yaml",
        shell=True
    )

def name_replacement(f_name, target_name, subdir_name):
    """ name_replacement """
    if not os.path.isfile(f_name):
        return
    shell(f"sed -i 's/colab-env/{target_name}/g' {f_name}", shell=True)
    shell(f"sed -i 's/colab_env/{subdir_name}/g' {f_name}", shell=True)

def add_short_description(target_name):
    """ add short description """
    description = input("Enter short description for repo: ")
    shell(
        f"sed -i 's/SHORT DESCRIPTION HERE/{description}/g' {target_name}/setup.py",
        shell=True
    )

def relocation(target_path):
    """ relocation """
    target_name = target_path.split("/")[-1]
    target_loc  = "/".join(target_path.split("/")[:-1])
    shell(f"mv {target_name}/* {target_path} --force", shell=True)
    shell(f"rm -r {target_name}", shell=True)

def main(target_path):
    """ main - top level of the script when properly invoked """
    ## get the names for the top and lower level directories
    target_name = target_path.split("/")[-1]
    subdir_name = "_".join(target_name.split("-"))
    ## generate a new directory copied from colab-env with the right name
    spawn_new_standard_repo(target_name, subdir_name)
    ## in the new directory replace all occurences of colab-env and colab_env
    target_contents = glob.glob(target_name+"/**", recursive=True)
    for f_name in target_contents:
        name_replacement(f_name, target_name, subdir_name)
    ## add short description to setup.py
    add_short_description(target_name)
    ## move the fully initialised directory to the correct place
    relocation(target_path)
    ## make a smooth exit...
    sys.exit()

if __name__ == "__main__":

    cmd_line_args = sys.argv

    if len(cmd_line_args) == 1:
        error_msg = (
            "\n"
            "No target for repo_setup!\n\n"
            "PROPER USAGE:\n\t"
            ">> python repo_setup.py /path/to/target-directory/"
            "\n"
        )

        sys.exit(error_msg)

    main(sys.argv[1])
