#this file must be called first at the
#start of the program
#it is the initialisation class that sets-up the begining of this vc

#imports
import os
import shelve
# orginalDirs = list()
class initialise:
    def __init__(self, cwd):
        self.cwd = cwd
    #start method
    #==> initialise.start()
    def start(self, cwd):
        paths = list()
        os.chdir(cwd)
        dir_shelve_path = "dirs_shelve.txt"
        filename_shelve_path = "filenames_shelve_path.txt"
        if os.path.exists(dir_shelve_path):
            pass
        else:
            os.mkdir(dir_shelve_path)
        if os.path.exists(filename_shelve_path):
            pass
        else:
            os.mkdir(filename_shelve_path)
        dirs = initialise.dirCacher(cwd)
        fileCaches = initialise.fileCahcer(cwd)
        #shelve contents of all lists to be used by add.
        dirShelf = shelve.open(dir_shelve_path)
        dirShelf['dirs'] = dirs
        dirShelf.close()
        fileCachesShelf = shelve.open(filename_shelve_path)
        fileCachesShelf['fileCaches'] = fileCaches
        fileCachesShelf.close()
        paths.append(dir_shelve_path, filename_shelve_path)
        return paths

    #method to find all files in file path
    def dirCacher(self, cwd):
        os.chdir(cwd)
        orginal_dirs = list()
        for folder, subfolder, file in os.walk():
            orginal_dirs.append(folder)
            orginal_dirs.append(file)
            orginal_dirs.append(file)
        return orginal_dirs
    #method to cache all contents of files
    def cache(self, filename):
        lines = list()
        self.filename = filename
        cacheFile = "cacheFile.txt"
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                with open(cacheFile, 'w') as fc:
                    fc.write(line)
                    fc.close()
            f.close()


    def fileCahcer(self, cwd):

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
        return filenames

