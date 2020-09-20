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
        Dirshelve = shelve.open(os.path.join(cwd, str(cacheDir) + str(cacheFile)))
        Dirshelve['dirs'] = dirsCache
        Dirshelve.close()
        FilesShelve = shelve.open(os.path.join(cwd, str(cacheDir) + str(cacheFile)))
        FilesShelve['files'] = filesCache
        FilesShelve.close()
        # todo: work on caching file content

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
