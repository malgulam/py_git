#! /usr/bin/python3.9

#imports
import os
import platform
import sys
sys.path.append('.')
from pygit import initialise
from pathlib import Path
from .exceptions import TrashPermissionError
from send2trash import send2trash
import argparse
from subprocess import Popen, PIPE, STDOUT

BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'
SHELF_DIR = BASE_DIR / 'python-git-shelf'
# STATUS_DIR = BASE_DIR / 'python-git-status'

#check whether os supports / has git present
def initialise(cwd=None):
    print('Initialising\npygit started')

def store_git_path(git_path):
    OS = detect_os()
    if OS != None:
        if git_exits(OS):
            print('Your system has been configured for git...')
def git_exits(osType):
    if 'Linux' or 'Ubuntu' or 'X' in osType:
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
    'Get command line argumets from terminal in unix based os/ cmd in windows'
    parser = argparse.ArgumentParser(prog="pygit")
    parser.add_argument("-v", "--verbosity", type=int, help="turn verbosity ON/OFF", choices=[0, 1])
    parser.add_argument("-r", "--rules", help="Set a list of string patterns for folders to skip during setup",
                        nargs='+')
    parser.add_argument('-g', '--gitPath', help="Full pathname to git executable. cmd or bash.")
    parser.add_argument('-m', '--masterDirectory', help="Full pathname to directory holding any number of git repos.")
    parser.add_argument('-s', '--simpleDirectory',
                        help="A list of full pathnames to any number of individual git repos.", nargs='+')
    parser.add_argument('-h', '--help', help="Display help message.")
    return parser.parse_args()


# commands class
class Commands:
    "Commands CLASS"
    "HANDLES EXECUTION OF COMMANDS FROM COMMANDLINES"
    def __str__(self):
        return "Commands: {}: {}".format(self.name, self.dir)
