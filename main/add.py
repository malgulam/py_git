#add class
#handle all adding of new files
#check changes
#imports
import os
import sys
import shelve
import sys
class add:
    def __init__(self):
        self = self


    #append function
    def append(self, filename, cwd):
        self.filename = filename
        self.cwd = cwd
        #original db lists
        original_files_list = list()
        original_dirs_list = list()
        #updated db lists
        updated_files_list = list()
        updated_dirs_list = list()
        cacheDir = "CacheDir/"
        cacheFile = "CachedDB"
        shelfCacheDB = os.path.join(cwd, str(cacheDir) + str(cacheFile))
        with shelve.open(shelfCacheDB) as db:
            for file in db['files']:
                original_files_list.append(file)
            for dir in db['dirs']:
                original_dirs_list.append(dir)
        #updating updated lists
        for root, dir, file in os.walk(self.cwd, topdown=False):
            updated_dirs_list.append(dir)
            updated_files_list.append(file)
        #checking for changes in dirs
        for dir in updated_dirs_list:
            if dir not in original_dirs_list:
                print(f"Woah you added DIRECTORY: {dir}")
                #opening the db with writeback to append new data
                db = shelve.open(shelfCacheDB, writeback=True)
                db['dirs'].append(file)
                db.close()
            else:
                pass
        #checking for changes in files
        for file in updated_files_list:
            if file not in original_files_list:
                print(f"Woah you added FILE: {file}")
                print(f"Added to the db")
                #opening the db with writeback to append new data
                db =  shelve.open(shelfCacheDB, writeback=True)
                db['files'].append(file)
                db.close()
            else:
                pass

    #main add function
    def add(self,cwd):
        self.cwd = cwd
        self.agrc = int(len(sys.argv))
        if self.agrc <= 1:
            print("Argument passed should be greater than 1")
            #print("Format: python3 PyGit.main.add.add(cwd=os.path.dirname(os.path.realpath(__file__))) {filename} \\ python3 PyGit.main.add.add(cwd=os.path.dirname(os.path.realpath(__file__))) .")
            print("Format: python3 add.py 'filename' ")
        else:
            pass

        #add all files to the existing db
        for i in range(self.agrc):
            add.append(self.sys.argv[i], cwd=self.cwd)









