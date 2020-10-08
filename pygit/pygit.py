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
import shelve
import shutil


BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'
SHELF_DIR = BASE_DIR / 'python-git-shelf'
# STATUS_DIR = BASE_DIR / 'python-git-status'


#check whether os supports / has git present
def initialise():
    print('Initialising\npygit started')
    try:
        os.mkdir(SHELF_DIR)
    except FileExistsError:
        shutil.rmtree(SHELF_DIR)
        Path.mkdir(SHELF_DIR)

    args = get_command_line_arguments()
    verbosity = args.verbosity
    rules = args.rules
    store_git_path(args.gitPath)
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
            return

        elif 'linux' or 'ubuntu' or 'x' in str(os.system("uname -a")).lower():
            path = retrieve_git_path(OS)
            # strore in shelf location
            SHELFDIROBJ = shelve.oepn(SHELF_DIR)
            SHELFDIROBJ['OS_TYPE'] = 'linux'
            SHELFDIROBJ['git_path'] = path
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
    #retrieving os type before carrying out further actions
    SHELFOBJ = shelve.
    os_type =
    def __str__(self):
        return "Commands: {}: {}".format(self.name, self.dir)

if __name__ == '__main__';
    initialise()