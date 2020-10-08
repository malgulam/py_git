#! /usr/bin/python3.9

#imports
import sys
sys.path.append('.')
from pygit import initialise
from pathlib import Path
from .exceptions import TrashPermissionError
from send2trash import send2trash
import argparse


BASE_DIR = Path.home()
DESKTOP = BASE_DIR / 'Desktop'

#check whether os supports / has git present
# def initialise(cwd=None):
#     print('Initialising')
#     inti_obj = initialise()

def get_command_line_arguments():
    'Get command line argumets from terminal in unix based os/ cmd in windows'


# commands class
class Commands:
    "Commands CLASS"
    "HANDLES EXECUTION OF COMMANDS FROM COMMANDLINES"
    def __str__(self):
        return "Commands: {}: {}".format(self.name, self.dir)
