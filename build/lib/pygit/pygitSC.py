#! /usr/bin/python3.9

#imports
import os
import platform
import sys

from pathlib import Path
import argparse
from subprocess import Popen, PIPE, STDOUT
import shelve
import shutil


BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'
SHELF_DIR = BASE_DIR / 'python-git-shelf'
# STATUS_DIR = BASE_DIR / 'python-git-status'


#check whether os supports / has git present
def initialise():
    print('Initialisialised')
    args = get_command_line_arguments()
    rules = args.rules
    path = store_git_path(retrieve_git_path(detect_os()))
    # shelve_master_directory(args.masterDirectory, rules)
    # shelve_simple_directory(args.simpleDirectory)
    #todo: set the initialize script to this
    print('Indexing done')
    return
def store_git_path(git_path):
    OS = detect_os()
    if OS != None:
        if git_exits(OS):
            print('Your system has been configured for git...')
        #working on windows machines
        if 'windows' in str(os.system("uname -a")).lower():
            path = retrieve_git_path(OS)
            #strore in shelf location
            SHELFDIROBJ = shelve.oepn(SHELF_DIR)
            SHELFDIROBJ['OS_TYPE'] = 'windows'
            SHELFDIROBJ['git_path'] = path
            print(path)
            return

        elif 'linux' or 'ubuntu' or 'x' in str(os.system("uname -a")).lower():
            path = retrieve_git_path(OS)
            # strore in shelf location
            SHELFDIROBJ = shelve.oepn(SHELF_DIR)
            SHELFDIROBJ['OS_TYPE'] = 'linux'
            SHELFDIROBJ['git_path'] = path
            print(path)
            return


def retrieve_git_path(operating_system):
    if 'linux' or 'ubuntu' or 'x' in str(operating_system).lower():
        #pretty simple for linux
        path = os.system("which  git")
        return  path

    if 'windows' in str(operating_system).lower():
        executable = "git"
        if os.path.sep in executable:
            raise ValueError("Invalid filename: %s" %executable)
        path = os.environ.get("PATH", "").split(os.pathsep)
        #Use path text to dtermine extensis executables may have
        path_exts = os.environ.get("PATHEXT", ".exe;.bat;.cmd").split(';')
        has_ext = os.path.splitext(executable)[1] in path_exts
        if not has_ext:
            exts = path_exts
        else:
            exts = [""]
        for d in path:
            try:
                for ext in exts:
                    exepath = os.path.join(d, executable + ext)
                    if os.access(exepath, os.X_OK):
                        return exepath
            except OSError:
                pass

            return None
    return sys.exit(1)
def git_exits(osType):
    if 'linux' or 'ubuntu' or 'x' in str(osType).lower():
        msg = os.system('git --version')
        if 'git version' in msg:
            print('git exists!Yay!')
            return True
        else:
            print('git not found on system.Exiting...')
            return False
            sys.exit(1)
    if 'windows' in str(osType).lower():
        proc = Popen(['git', '--version'], shell=True, stdout=PIPE, )
        msg, _ = proc.communicate()
        msg = msg.decode('utf-8')
        if "git version" in msg:
            return True
        return False



def detect_os():
    if os.name == "posix":
        ostype = os.system("uname -a")
        print(ostype)
        return ostype
    else:
        print("unknown OS")
        sys.exit(1)
def get_command_line_arguments():
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(prog="Pygit. Initialize working directories for python-git")
    parser.add_argument('-m', '--masterDir', help="Full path to local git repo.")
    #todo: add more functionality to a_a
    parser.add_argument('-a_a', '--automate_actions(request)', help="Automate request and render actions.Example:--automate_actions(push)")
    return parser.parse_args()



#working on commands
command = str(sys.argv[1]).replace('--', '')
#todo: create function that runs commands passed to sys.argv[1]
print(command)
if __name__ == '__main__':
    initialise()