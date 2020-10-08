![Image of PyGit Logo](https://github.com/malgulam/PyGit/blob/master/pygit/PyGitLogo.png) 
# PyGit
## Python Git-like VC Tool For Code Debug Purposes.
### This package acts as a version control tool that helps python developers to create,edit,modify and reformat code from within the program itself.
 -  This program stores roots, directories and filenames to sql database.
 -  This program caches file contents
 -  This program outputs differences between current and previous code files.
 - Performs simple code comparisons

```python
**code.py**
---------------------------------------------------------------------------------------------------
import logging
from sys.path.append('.')
import PyGit
from PyGit import initialise, autonomize
#!/usr/python3

#setting up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logging.warning('Watch out!')  # will print a message to the console
#setting up pygit debug
autonomize.autonomize().autonomize(cwd=os.path.dirname(os.path.realpath(__file__)))
#initialise.initialise().initialise(cwd=os.path.dirname(os.path.realpath(__file__)))
def wish_me(name):
    print('Happy Birthday', name)
usrinp = input('name: ')
print(wish_me(usrinp))

```
## Requirements:
 - Python3+
 - Directory name of realpath of current working file as shown in the code samples one line 15 and 16.
 - Linux based operating system.This is as a result of the default file handling operations carried out.This can be modified to run on Windows OS.
 - At least 2GB of RAM.
 - At least 32 GB of storage.
 ```python
     autonomize.autonomize().autonomize(cwd=os.path.dirname(os.path.realpath(__file__)))
    initialise.initialise().initialise(cwd=os.path.dirname(os.path.realpath(__file__)))
 ```
**NB:**
 - Use initialise script on first run to cache all required files, folders and roots into SQL Database.
 - Run autonomize to perform the above condition with just the push of  a button.

 - Contribute!

*Check out pypi @druzgeorge @agulam-coco*



**Much contribution will be needed.Thanks in advance. :]**
