#this file must be called first at the
#start of the program
#it is the initialisation class that sets-up the begining of this vc

#imports
import os
import shelve
orginalDirs = list()
class initialise:
    def __init__(self, filePath):
        self.filePath = filePath
        os.chdir(filePath)
    #method to find all files in file path
    def dirCacher(self, cwd):
        global orginalDirs
        self.cwd = cwd
        os.chdir(cwd)
        orginal_dirs = list()
        for folder, subfolder, file in os.walk():
            orginal_dirs.append(folder)
            orginal_dirs.append(file)
            orginal_dirs.append(file)
            orginalDirs.append(folder)
            orginalDirs.append(file)
            orginalDirs.append(file)
        return orginalDirs
    #method to cache all contents of files
    def cache(self, filename):
        self.filename = filename
        cacheFile = "cacheFile.txt"
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in  lines:
                with open(cacheFile, 'w') as fc:
                    fc.write(line)
                    fc.close()
            f.close()


    def fileCahcer(self):
        all_dir = os.listdir()
        filenames =  list()
        for i in range(len(all_dir)):
            if "." in str(all_dir[i]):
                filenames.append(all_dir[i])
            else:
                pass
        #cache contents
        for i in range(len(filenames)):
            initialise.cache(filenames[i])
