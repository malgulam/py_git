#commands class to handle the commands and execution of commands

#imports
import sys
sys.path.append('PyGit/')
from pygit import DESKTOP, SHELF_DIR
import os
import shelve 
import PySimpleGUI as sg
from colorit import *
from pathlib import Path
import shutil
from core.WindowsSupport import WindowsSupport

#Commands Class
class Commands(object):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __str__(self):
        return ('Commands {} {}'.format(self.name,self.dir) )

    def __init__(self, windows_support=False, argument=None, argument_content=None):
        self.argument = argument
        self.argument_content = argument_content
        self.windows_support = windows_support
        #passing arguments to WindowsSupport Class if windows_support == True
        if windows_support == True:
            WindowsSupportObj = WindowsSupport(activate=True, argument=self.argument, argument_content=self.argument_content)
        Commands.recognize_commands(self, self.argument, self.argument_content)
    def recognize_commands(self, argument, argument_content):
        self.argument = argument
        self.argument_content = argument_content
        print(self.argument, self.argument_content)
        #redirecting to respective function
        if self.argument == 'masterDir':
            Commands.index_master(self.argument_content)
        elif self.argument == 'automate_actions':
            Commands.automate_actions(action=self.argument_content)
        elif self.argument == 'clone':
            Commands.clone(url=self.argument_content)
        elif self.argument == 'init':
            Commands.init(cwd=self.argument_content)
        elif  self.argument == 'push':
            Commands.push(path=os.getcwd())
        elif self.argument == 'set_global_credentials':
            print(self.argument_content)
            Commands.set_globals(self.argument_content)
        elif self.argument == 'add':
            Commands.add(self.argument_content)

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
                Commands.push(path=os.getcwd())
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
        sg.theme('SandyBeach')
        layout = [
            [sg.Text("This is very dangerous!")],
            [sg.Text("Setting credentials to global is efficent but insecure.\nYour information will be stored in "
                          f"{SHELF_DIR} as a shelve file.\nYou can proceed but it is advised to "
                          f"setup SSH keys for your github to avoid using this.\nRead this:'https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account'"
                          )],
            [sg.Text("Do you wish to continue?")],
            [sg.Yes(), sg.No()]
                        
        ]
        window = sg.Window('WARNING', layout)
        event, values = window.read()
        window.close()
        # print(color_front("This is very dangerous!", red=255, green=0, blue=0))
        # print(color_front("Setting credentials to global is efficent but insecure.\nYour information will be stored in "
        #                   f"{SHELF_DIR} as a shelve file.\nYou can proceed but it is advised to "
        #                   f"setup SSH keys for your github to avoid using this.\nRead this:{color_front('https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account', red=0, green=255, blue=0)}"
        #                   , red=255, green=0, blue=0))
        opt = event
        opt = opt.lower()
        if opt ==  "yes":
            print("Working...")
            try:
                Commands.safe_mkdir(SHELF_DIR)
                print('credentials', credentials)
                # so password is gloablcredentilas[1] and username is [0]
                Commands.shelfer(key='global_credentials', content=credentials)
            except FileExistsError:
                shutil.rmtree(SHELF_DIR)
                Commands.safe_mkdir(SHELF_DIR)
                # so password is gloablcredentilas[1] and username is [0]
                Commands.shelfer(key='global_credentials', content=credentials)
            print("Done...")
            return
        elif opt == 'no':
            print(color_front("Aborted!", red=255, green=0, blue=0))
            print(color_front(f"Read: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account ", red=0, green=150, blue=240) ,color_front("On how to perform adding SSH key to account", 255,255,255))
            sys.exit(1)
        else:
            print('error!')
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
        Commands.init(cwd=os.getcwd())
        Commands.shelfer(key="master_repo", content=path_to_master_local_repo)
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
