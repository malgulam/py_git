#imports
import os
from pygit import DESKTOP
import os
import shelve 
from colorit import *
from pathlib import Path
import shutil


class WindowsSupport(object):
    WINDOWS_GIT_PATH = ''
    def __init__(self, activate=False, argument=None, argument_content=None):
        self.activate = activate
        if self.activate == False:
            print('Windows Support disabled')
        print('Windows Support Activated')
        if not WindowsSupport.retrieve_windows_git_path():
            print('git not found on windows system.')
            sys.exit(1)
        WindowsSupport.recognize_commands(self, self.argument, self.argument_content)
    #boolean function
    def retrieve_windows_git_path():
        pass
    def recognize_commands(self, argument, argument_content):
        self.argument = argument
        self.argument_content = argument_content
        print(self.argument, self.argument_content)
        #redirecting to respective function
        if self.argument == 'masterDir':
            WindowsSupport.index_master(self.argument_content)
        elif self.argument == 'automate_actions':
            WindowsSupport.automate_actions(action=self.argument_content)
        elif self.argument == 'clone':
            WindowsSupport.clone(url=self.argument_content)
        elif self.argument == 'init':
            WindowsSupport.init(cwd=self.argument_content)
        elif  self.argument == 'push':
            WindowsSupport.push(path=os.getcwd())
        elif self.argument == 'set_global_credentials':
            print(self.argument_content)
            WindowsSupport.set_globals(self.argument_content)
        elif self.argument == 'add':
            WindowsSupport.add(self.argument_content)

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
                WindowsSupport.push(path=os.getcwd())
        else:
            return "Unknown action {}".format(action)

    @staticmethod
    def add(mode):
        if mode == '.':
            print('Add all mode.Resulting to git.')
            os.system("git add .")
        print("Adding {} to index...".format(mode))
        os.system("git add {}".format(mode))
        print('done')
        return

    @staticmethod
    def set_globals(username_password):
        #todo: fix yes or no query
        #todo: fix b'globalcredentials' KeyError problem
        #spliting username_password into a list separated by ','
        credentials = str(username_password).split('/')
        #making sure coloit will be usable in commandline interfaces
        print(color_front("This is very dangerous!", red=255, green=0, blue=0))
        print(color_front("Setting credentials to global is efficent but insecure.\nYour information will be stored in "
                          f"{SHELF_DIR} as a shelve file.\nYou can proceed but it is advised to "
                          f"setup SSH keys for your github to avoid using this.\nRead this:{color_front('https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account', red=0, green=255, blue=0)}"
                          , red=255, green=0, blue=0))
        opt = input(f"\n\nDO YOU WISH TO PROCEED? y(Y)es/n(N)o: ")
        opt = opt.lower()
        if opt == "y" or "yes":
            print("Working...")
            try:
                WindowsSupport.safe_mkdir(SHELF_DIR)
                print('credentials', credentials)
                # so password is gloablcredentilas[1] and username is [0]
                WindowsSupport.shelfer(key='global_credentials', content=credentials)
            except FileExistsError:
                shutil.rmtree(SHELF_DIR)
                WindowsSupport.safe_mkdir(SHELF_DIR)
                # so password is gloablcredentilas[1] and username is [0]
                WindowsSupport.shelfer(key='global_credentials', content=credentials)
            print("Done...")
            return
        else:
            print(color_front("Aborted!", red=255, green=0, blue=0))
            print(color_front("Read: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account \n On how to perform adding SSH key to account", red=0, green=150, blue=240))
            sys.exit(1)
    @staticmethod
    def init(cwd):
        os.chdir(cwd)
        os.system("git init")
        print("initialised git!")
        return
    @staticmethod
    def index_master(path_to_master_local_repo):
        os.chdir(path_to_master_local_repo)
        WindowsSupport.init(cwd=os.getcwd())
        WindowsSupport.shelfer(key="master_repo", content=path_to_master_local_repo)
        print('MasterIndexed')
        return
    @staticmethod
    def clone(url, path=DESKTOP):
        print("Cloning to Desktop")
        cwd = os.getcwd()
        os.chdir(path)
        os.system("git clone {}".format(url))
        os.chdir(cwd)
        return
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
    @staticmethod
    def shelfer(key="masterKey", content=None):
        shelve_file_path = os.path.join(str(SHELF_DIR), 'pygit_shelve')
        shelfobj = shelve.open(shelve_file_path)
        shelfobj[key] = content
        shelfobj.close()
        return

    