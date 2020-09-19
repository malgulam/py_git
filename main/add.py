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
        print(f"{number_file_changes} files  made!")
        print(f"{number_dir_changes} dir created / changed!")
        #checking for differences in file
        #content
        with shelve.open(filename_shelfPath) as db:
            for i in range(len(updated_dirs)):
                if "." in str(updated_dirs[i]):
                    if str(updated_dirs[i]) not in file_changes:
                        cacheFile = str(updated_dirs[i])+'_cacheFile.txt'
                        newFile = str(updated_dirs[i])
                        with open(cacheFile) as f1:
                            with open(newFile) as f2:
                                fileList1 = f1.read().splitlines()
                                fileList2 = f2.read().splitlines()
                                list1length = len(fileList1)
                                list1length = len(fileList2)
                                if fileList1 == fileList2:
                                    for index in range(len(fileList1)):
                                        if fileList1[index] == fileList2[index]:
                                            print(fileList1[index] + "==" + fileList2[index])
                                        else:
                                            print(fileList1[index] + "!=" + fileList2[index] + " Not-Equel")
                                    else:
                                        print ("difference inthe size of the file and number of lines")

                    else:
                        pass
                else:
                    pass





