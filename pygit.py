#imports
import os
import sys
sys.path.append('PyGit/')
from colorit import *
from pathlib import Path
import argparse
from subprocess import Popen, PIPE
import shelve
import shutil
from core.Commands import Commands
from core.WindowsSupport import WindowsSupport

BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'
SHELF_DIR = str(BASE_DIR) +'/'+ 'python-git-shelf'

#todo: fix winows support
#initialise the program
def initialise():
    print('Initialising....')
    #check if system supports git
    osType = detect_os()
    if 'windows' in str(osType).lower():
        WindowsOSObj = WindowsSupport(activate=True)
    if not git_exists(osType):
        sys.exit(1)
    print('System supports git!')
    args = get_commandline_arguments()
    push = args.push
    set_global_credentials = args.set_global_credentials
    masterDir = args.masterDir
    automate_actions = args.automate_actions
    clone = args.clone
    init = args.init
    add = args.add
    commands = ['masterDir', "automate_actions", "clone", "init", "push", "set_global_credentials", "add"]
    commands_arg_content = [masterDir, automate_actions, clone, init, push, set_global_credentials, add]
    for command_arg_content in commands_arg_content:
        if command_arg_content:
            #pass commands list the index fothe command_Arg_content item to get it's respective command
            CommandsObj = Commands(windows_support=False,argument=commands[commands_arg_content.index(command_arg_content)],argument_content=command_arg_content)
        else:
            pass



def detect_os():
    if os.name == "posix":
        ostype = os.uname()[0]
        print('OS: ', ostype)
        return ostype
    else:
        print("unknown OS")
        print('exiting...')
        sys.exit(1)

def git_exists(osType):
    if 'linux' or 'ubuntu' or 'x' in str(osType).lower():
        #in linux if you run os.system("git --version it prints git version and return code of 0")
        msg = os.system("git --version")
        if msg == 0:
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
            print('git exists!Yay!')
            return True
        return False

def get_commandline_arguments():
    "Print command_line_arguments help"
    try:
        parser = argparse.ArgumentParser(prog="pygit. Initialise pygit by running python3 pygit --init / -i {cwd}.Where cwd is the full path to the directory you want to initialise pygit in.")
        parser.add_argument('-s_g_c', '--set_global_credentials', help="set global your credentials.Please use a developer's token as the password.\nFormat: python3 -m pygit --set_global_credentials username/password.\nExample:python3 -m pygit --set_global_credentials bobbyBoy/8whagdjeuanhdjd"
                                                                       "Advise you setup ssh method of git access with your pc to avoid usage.")
        parser.add_argument('-m', '--masterDir',  help="Full path to local git repo containining many other sub-directories")
        parser.add_argument('-a_a', '--automate_actions', help="Automates the process of performing simple git actions\nExample: --automate_actions[push, pull, fetch, commit]")
        parser.add_argument('-p', '--push', help='Push new code / builds to remote git repo')
        parser.add_argument('-c', '--clone', help='Clone remote git repo.Example: python3 pygit.py --clone {url}\nDownload Path is set to default at Desktop')
        parser.add_argument('-i', '--init', help='Initialise pygit in local repo.Example: python3 pygit --init {cwd}.Where cwd is the full path to the directory you want to initialise pygit in.')
        parser.add_argument('-a', '--add', help="Add file contents to the index.Usage: python3 -m pygit add .")
        return parser.parse_args()
    except argparse.ArgumentError as e:
        print('Unknown argument')




if __name__ == '__main__':
    initialise()