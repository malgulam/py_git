# this file must be called first at the
# start of the program
# it is the initialisation class that sets-up the begining of this vc

# imports
import os
import shelve


# orginalDirs = list()
class initialise:
    def __init__(self):
        self = self

    def start(self, cwd):

        # creating cache dirs
        self.cwd = cwd
        print(self.cwd)
        cacheDir = "CacheDir/"
        if os.path.exists(os.path.join(cwd, cacheDir)):
            pass
        else:
            os.mkdir(os.path.join(cwd, cacheDir))
        # Creating db for caching the current dirs and filenames
        cacheFile = "CachedDB"
        dirsCache = initialise.dirCacher(self, cwd=self.cwd)
        filesCache = initialise.filesCacher(self, cwd=self.cwd)
        dirsCacheFile = "dirCacheFile"
        # saving dir cacher to shelf file
        dirs_shelve_path = os.path.join(cwd, str(cacheDir) + str(cacheFile))
        Dirshelve = shelve.open(dirs_shelve_path)
        Dirshelve['dirs'] = dirsCache
        Dirshelve.close()
        files_shelve_path = os.path.join(cwd, str(cacheDir) + str(cacheFile))
        FilesShelve = shelve.open(files_shelve_path) #todo: next time just set all the variables for this
                                                    #path to one name becase the open the same file anyway
        FilesShelve['files'] = filesCache
        FilesShelve.close()
        # absolute_cache_dir = str(self.cwd)+ str(cacheDir)
        absolute_cache_dir = f"{self.cwd}/{cacheDir}"
        # todo: work on caching file content
        initialise.fileContentCacher(self, cwd=self.cwd, cacheDir=absolute_cache_dir,dirsDB=dirs_shelve_path, filesDB=files_shelve_path)

    def dirCacher(self, cwd):
        self.cwd = cwd
        dirs = list()
        for root, dir, files in os.walk(self.cwd, topdown=False):
            dirs.append(dir)
        return dirs

    def filesCacher(self, cwd):
        cwd = self.cwd
        filenames = list()
        for root, dir, file in os.walk(self.cwd, topdown=False):
            filenames.append(file)
        return filenames

    def fileContentCacher(self, cwd, cacheDir,dirsDB, filesDB):
        self.cwd = cwd
        self.dirsDB = dirsDB
        self.filesDB = filesDB
        self.cacheDir = cacheDir
        dirs = list()
        filenames = list()
        dirsShelfer = shelve.open(self.dirsDB)
        for dir in dirsShelfer['dirs']:
            dirs.append(dir)
        dirsShelfer.close()
        FilesShelfer = shelve.open(self.filesDB)
        for file in FilesShelfer['files']:
            filenames.append(file)
        FilesShelfer.close()
        #finding whether filenames exists
        for i in range(len(filenames)):
            for file in filenames[i]:
                for i in range(len(dirs)):
                    for dir in dirs[i]:
                        path = f"{self.cwd}/{dir}/{file}"
                        if os.path.exists(path):
                            print(path)
                            lines = list()
                            cacheFileName = str(file)+"_cacheFile.txt"
                            #reading content of file
                            try:
                                with open(path, "r") as f:
                                    lines = f.readlines()
                                f.close()
                                # cache_file_absolute_path = self.cacheDir+str(cacheFileName)
                                print(self.cacheDir)
                                cache_file_absolute_path = f"{self.cacheDir}{cacheFileName}"
                                with open(cache_file_absolute_path, "w+") as f:
                                    for line in lines:
                                        # f.write(f"{line}".decode('utf-8') + "\n")
                                        f.write(f"{line}" + "\n")
                                f.close()
                            except UnicodeDecodeError as e:
                                print("encountered unicode decode error")
                            break
                        else:
                            pass

        #searching for path fo the file
        #then cache the file
        # for i in range(len(filenames)):
        #     for file in filenames[i]:
        #         lines = list()
        #         cacheFileName = str(file)+"_cacheFile.txt"
        #         #getting path of file
        #         print("FILE")
        #         print(file)
        #         path_to_file = os.path.dirname(os.path.abspath(f"__{file}__"))
        #         print(str(path_to_file))
        #         print(file)
        #         # absolute_path = str(path_to_file)+str(f"/{file}")
        #         absolute_path = os.path.dirname(os.path.realpath(f"__{file}__"))
        #         #reading content of file
        #         with open(absolute_path, "r") as f:
        #             lines = f.readlines()
        #         f.close()
        #         cache_file_absolute_path = self.cacheDir+str(cacheFileName)
        #         with open(cache_file_absolute_path, "w+") as f:
        #             f.write(lines)
        #         f.close()




