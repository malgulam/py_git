#PyGit __init__.py
from .__version__ import __version__
import sys
sys.path.append('.')
from py_git import pygit
initialise = pygit.initialise()

