#this file must be called first at the
#start of the program
#it is the initialisation class that sets-up the begining of this vc

#imports
import os
import shelve
# orginalDirs = list()
class initialise:
    def __init__(self):
        #TODO: REMIND USER TO SET ORIGINAL_FILES, ORIGINAL_DIRS TO NULL
        #TODO:Find something to do here
        self = self

    #start method
    #==> initialise.start()
    def start(self, cwd):
        self.cwd = cwd
        paths = list()
        os.chdir(cwd)
        dir_shelve_path = "dirs_shelve_dir/"
        filename_shelve_path = "filenames_shelve_dir/"
        if os.path.exists(dir_shelve_path):
            pass
        else:
            os.mkdir(dir_shelve_path)
        if os.path.exists(filename_shelve_path):
            pass
        else:
            os.mkdir(filename_shelve_path)
        dirs = initialise().dirCacher(cwd)
        fileCaches = initialise().fileCacher(cwd)
        #shelve contents of all lists to be used by add.
        dirShelf = shelve.open(str(dir_shelve_path)+'dir_shelve')
        dirShelf['dirs'] = dirs
        dirShelf.close()
        fileCachesShelf = shelve.open(str(filename_shelve_path)+'filenamescache')
        fileCachesShelf['fileCaches'] = fileCaches
        fileCachesShelf.close()
        # paths.append(dir_shelve_path, filename_shelve_path)
        return dir_shelve_path, filename_shelve_path

    # TODO: handle caching of all current files, folders and subfolders
    # TODO:set return type to multi return eg.) return dirlist, filenameslist
    # TODO: handle this new return type in the start method

    def dirCacher(self,cwd):
        original_dirs = list()
        for root, dirs, files in os.walk(".", topdown=False):
            dirs.append(dirs)
        return original_dirs

    #TODO: copy the below method into line 61 as a code bloc
    def cacher(self, cwd, filename):
        #TODO: find more efficient way to iterate through characters
        #Todo:to find last dot to find file extension
        # dotList = []
        # for i in range(len(filename)):
        #     if filename[i] == ".":
        #         dotList.append(i)
        #     else:
        #         pass
        # newFilename_without_extension = f"{filename[:dotList[-1]]}"
        # cacherFile_name = f"{newFilename_without_extension}_cacheFile.txt"
        # cacherDirPATH = "CacherDir/"
        # lines = list()
        # with open(f"{cwd}/{filena}")
        dotList = list()
        lines = list()
        #get actual filename
        for i in range(len(filename)):
            if filename[i] == ".":
                dotList.append(i)
            else:
                pass
        #TODO: make try except block for cachedir
        dirs_list = list()
        cacheDirPath = "CacheDir/"
        # try:
        #     os.mkdir(cacheDirPath)
        # except FileExistsError:
        #     pass
        # except OSError as e:
        if os.path.exists(cwd+cacheDirPath):
            os.mkdir(os.path.join(cwd, cacheDirPath))
        else:
            pass
        print(filename)
        cache_filename = f'{filename[:dotList[-1]]}_cacheFile.txt'
        for root, subfolder, file in os.walk(cwd, topdown=False):
            dirs_list.append(subfolder)
        #checking whether file exists
        for i in range(len(dirs_list)):
            # os.path.join(dirs_list[i], filename)
            if os.path.exists(f"{dirs_list[i]}/{filename}"):
                with open(os.path.join(dirs_list[i], filename), "r") as f:
                    lines = f.readlines()
                f.close()
            else:
                pass
        with open(cache_filename, "w+") as f:
            for i in range(len(lines)):
                f.write(lines[i])
        f.close()

    def file_content_cacher(self, cwd, filenames, dirs):
        for files in filenames:
            for i in range(len(dirs)):
                if os.path.exists(f"{dirs[i]}/{files})"):
                    accepted_path = str(dirs[i])+"/"+str(files)
                    initialise().cacher(cwd=cwd, filename=accepted_path)
                else:
                    pass



    def fileCacher(self, cwd):
        original_files = list()
        dirs = list()
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            original_files.append(files)
            dirs.append(dirs)
        #actual cacher method
        for file in original_files:
            initialise().file_content_cacher(cwd, file, dirs)
        return original_files