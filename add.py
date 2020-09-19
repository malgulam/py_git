#add.py

from __future__ import with_statement
import os

def add(orginalFiles):
    filenames = os.listdir()
    newFiles = list()
    for i in range(originalFiles):
        if f"originalFiles[i]" == f"{filenames[i]}":
            pass
        else:
            newFiles.append(filenames[i])
    return newFiles 

