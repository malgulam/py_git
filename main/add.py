#add class
#handle all adding of new files
#check changes
#imports
import os
import sys
import shelve
import initialise
class addClass:
    def __init__(self, filename, cwd):
        self.filename = filename
        self.cwd = cwd
    def add(self, presentCWD):
        #TODO: get list of dirs in this cwd
        updated_dirs = os.listdir()
        #changes dir list
        dir_changes = list()
        #changes files list
        file_changes = list()
        #handling orginal files
        #cross-checking with new dir
        paths = initialise.initialise.start(cwd=presentCWD)
        shelves = {"dir":f"{paths[0]}", "files":f"{paths[1]}"}
        dirs_shelfPath = shelve.open(shelves["dir"])
        filename_shelfPath = shelve.open(shelves["files"])

        #checking for changes
        with shelve.open(dirs_shelfPath) as db:
            for i in range(len(updated_dirs)):
                if updated_dirs[i] not in db["dirs"]:
                    dir_changes.append(updated_dirs[i])
            shelve.close(dirs_shelfPath)
        with shelve.open(filename_shelfPath) as db:
            for folder, subfolder, file in os.walk():
                if file not in db["fileCaches"]:
                    file_changes.append(file)
            shelve.close(filename_shelfPath)
        number_file_changes = len(file_changes)
        number_dir_changes = len(dir_changes)
        print(f"{number_file_changes} file changes made!")
        print(f"{number_dir_changes} dir created / changed!")




