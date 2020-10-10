#imports
import os
import sys
sys.path.append(os.getcwd())
from colorit import *
from pathlib import Path
import argparse
from subprocess import Popen, PIPE
import shelve
import shutil

BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'
SHELF_DIR = BASE_DIR / 'python-git-shelf'

#todo: fix winows support
#initialise the program
def initialise():
    print('Initialising....')
    #todo: search whether the git shelf is empty before doing all this to prevent annoying prompts
    #check if system supports git
    osType = detect_os()
    if not git_exists(osType):
        sys.exit(1)
    print('System supports git!')
    args = get_commandline_arguments()
    #todo: if you make changes to commands list make changes to self.commands in the recognize_commands in class Commands:
    push = args.push
    set_global_credentials = args.set_global_credentials
    masterDir = args.masterDir
    automate_actions = args.automate_actions
    clone = args.clone
    init = args.init
    commands = ['masterDir', "automate_actions", "clone", "init", "push", "set_global_credentials"]
    commands_arg_content = [masterDir, automate_actions, clone, init, push, set_global_credentials]
    for command_arg_content in commands_arg_content:
        if command_arg_content:
            #pass commands list the index fothe command_Arg_content item to get it's respective command
            CommandsObj = Commands(commands[commands_arg_content.index(command_arg_content)],command_arg_content)
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
        return parser.parse_args()
    except argparse.ArgumentError as e:
        print('Unknown argument')



#todo: create commands to deal with command related issues

class Commands(object):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __str__(self):
        return ('Commands {} {}'.format(self.name,self.dir) )

    def __init__(self, argument, argument_content):
        self.argument = argument
        self.argument_content = argument_content
        Commands.recognize_commands(self, self.argument, self.argument_content)
    def recognize_commands(self, argument, argument_content):
        self.argument = argument
        self.argument_content = argument_content
        print(self.argument, self.argument_content)
        #below is a list of k,v items in a commands dict which maps each command to it's respectiive function!
        # self.commands = {'masterDir':"index_master()", "automate_actions":"automate_actions()", "clone":"clone()", "init":"init()", "push":"push()", "set_global_credentials":"set_globals()"}
        #todo: redirect every argument to it's static function
        #redirecting to respective function
        if self.argument == 'masterDir':
            Commands.index_master()
        elif self.argument == 'automate_actions':
            Commands.automate_actions(action=self.argument_content)
        elif self.argument == 'clone':
            Commands.clone(url=self.argument_content)
        elif self.argument == 'init':
            Commands.init(cwd=self.argument_content)
        elif  self.argument == 'push':
            Commands.push()
        elif self.argument == 'set_global_credentials':
            Commands.set_globals(self.argument_content)

    @staticmethod
    def automate_actions(action, commit_msg="new changes"):
        #todo: set actions to all possible automate actions
        actions = ['push', 'clone']
        #if the action in actions ? redirect to distinct func : return error
        if action in actions:
            if action == 'push':
                os.system("git pull")
                os.system("git add .")
                os.system("git status")
                os.system(f"git commit -m '{commit_msg}.Pushed with automate_actions'")
                Commands.push(os.getcwd())
        else:
            return "Unknown action {}".format(action)
    @staticmethod
    def set_globals(username_password):
        # todo: add warning message to set_globals showing this option is not secure
        # todo: let user pass passwords and username like 'username/password' so you can use .split(/) to
        # todo: retrive both username and password from a declared list
        #spliting username_password into a list separated by ','
        credentials = str(username_password).split('/')
        #making sure coloit will be usable in commandline interfaces
        print(color_front("This is very dangerous!", red=255, green=0, blue=0))
        print(color_front("Setting credentials to global is efficent but insecure.\nYour information will be stored in "
                          f"{SHELF_DIR} as a shelve file.\nYou can proceed but it is advised to "
                          f"setup SSH keys for your github to avoid using this.\nRead this:{color_front('https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account', red=0, green=255, blue=0)}"
                          , red=255, green=0, blue=0))
        opt = str(input(f"\n\nDO YOU WISH TO PROCEED? y(Y)es/n(N)o: ")).lower()
        # print(opt.lower())
        if opt == "y" or "yes":
            print("Working...")
            try:
                Commands.safe_mkdir(SHELF_DIR)
                shelveOBJ = shelve.open(SHELF_DIR)
                shelveOBJ['gloabal_credentials'] = credentials[0]
                shelveOBJ['global_credentials'].append(credentials[1])
                shelveOBJ.close()
            except FileExistsError:
                shutil.rmtree(SHELF_DIR)
                Commands.safe_mkdir(SHELF_DIR)
                shelveOBJ = shelve.open(SHELF_DIR)
                shelveOBJ['gloabal_credentials'] = credentials[0]
                shelveOBJ['global_credentials'].append(credentials[1])
                shelveOBJ.close()
            print("Done...")
            return
        else:
            print(color_front("Aborted!", red=255, green=0, blue=0))
            print(color_front("Read: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account \n On how to perform adding SSH key to account", red=0, green=150, blue=240))
            sys.exit(1)
    @staticmethod
    def init():
        #todo: set path to cwd
        os.system()
    @staticmethod
    def index_master():
        pass
    @staticmethod
    def clone(url, path=DESKTOP):
        os.system("git clone {}".format(url))
    @staticmethod
    def push(path):
        print("Pushing new code")
        os.system("git push")
    @staticmethod
    def safe_mkdir(path):
        print("Initialised safe_mkdir()\n Making dir in safe mode.")
        if not os.path.exists(path):
            os.mkdir(path)
            print("Directory successfully created at {}".format(path))
            return
        shutil.rmtree(path)
        os.mkdir(path)
        print("Directory successfully created at {}".format(path))
        return
if __name__ == '__main__':
    initialise()