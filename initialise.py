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
        paths.append(dir_shelve_path, filename_shelve_path)
        return paths

    # TODO: handle caching of all current files, folders and subfolders
    # TODO:set return type to multi return eg.) return dirlist, filenameslist
    # TODO: handle this new return type in the start method

    def dirCacher(self,cwd):
        original_dirs = list()
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            dirs.append(dirs)
        return original_dirs

    #TODO: copy the below method into line 61 as a code bloc
    def cacher(self, cwd, filename):
        cacher_file = str(filename) +"_chacheFile.txt"
        #TODO: MAKE A CACHER DIR
        CacherDirPath = "CacherDir/"
        lines = list()
        with open(f"{cwd}/{filename}",  "r") as f:
            lines = f.readlines()
        f.close()
        #TODO: wite to the file in the cacher dir with the same name as original
        #todo: file but ends with _cacheFile.txt
        # if os.path.exists(CacherDirPath):
        #     pass
        # else:
        #     print("does not exists")
        #     os.mkdir(str(cwd)+CacherDirPath)
        # with open(str(CacherDirPath)+cacher_file, "w+") as f:
        #     f.write(lines)
        # f.close()
        if os.path.exists(str(cwd)+'/'+CacherDirPath):
            pass
        else:
            os.mkdir(str(cwd)+'/'+CacherDirPath)
        f =open(str(cwd)+'/'+CacherDirPath+cacher_file, "w")
        f.write(lines)
        f.close()

    def file_content_cacher(self, cwd, filenames, dirs):
        #TODO:search for files dir,  copy the content
        for files in filenames:
            #Todo: iterate through original_dirs to find if when con
            #cancerated the file path exists
            # for dir in dirs:
            #     for i in range(len(filenames)):
            #         if os.path.exists(os.path.join(dir, filenames[i])):
            #             initialise().cacher(cwd=cwd, filename=str(dir)+"/"+str(filenames[i]))
            #         else:
            #             pass
            for i in range(len(dirs)):
                if os.path.isfile(os.path.join(dirs[i], files)):
                    accepted_path = str(dirs[i])+"/"+str(files)
                    initialise().cacher(cwd=cwd, filename=accepted_path)
                else:
                    pass


        #TODO:create file to write cached content into
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