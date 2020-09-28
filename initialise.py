#!/usr/bin/python3
#initialise class
#imports
import os
import sqlite3

class initialise:
    def __init__(self):
        self = self
    def initialise(self, cwd):
        #TODO: set the path of cache to caches instead
        #todo: set the caches to increment to make this_cache.txt increase when cachedagain this_cache1.txt
        self.cwd = cwd
        #create cache dir
        cachedDir = "Caches/"
        #checking whether the cache  dir exists
        try:
            os.mkdir(os.path.join(cwd, cachedDir))
        except FileExistsError as e:
            #cache dir already present
            pass
        #making cachedb
        files_dirsCache = f"{cachedDir}F_DCache.db"
        try:
            open(files_dirsCache, 'a').close()
        except FileExistsError as e :
            #F_DCache file exists
            pass
        #lists for db commits
        roots = list()
        dirs = list()
        files = list()
        #walking through the dir to harvest data
        for root, dir, file in os.walk(cwd, topdown=False):
            roots.append(root)
            dirs.append(dir)
            files.append(file)
        #creating files and dirs File list cache
        #using sqlite3
        # conn = None
        try:
            conn = sqlite3.connect(files_dirsCache)
            # cursor c
            c = conn.cursor()
            #Create table
            # c.execute('''CREATE TABLE dirs_files
            #                    (Roots, Dirs, Files, CachedPaths)''')
            c.execute('''CREATE TABLE IF NOT EXISTS dirs_files(Roots TEXT, Dirs TEXT, Files TEXT, CachedPaths TEXT)''')
        except sqlite3.Error as e:
            print(e)
        try:
            # inserting data
            # inserting the roots
            for i in range(len(roots)):
                for root in roots[i]:
                    c.execute(f"INSERT INTO dirs_files(Roots) VALUES(?)", (root,))
            # inserting dirs
            for i in range(len(dirs)):
                for dir in dirs[i]:
                    c.execute(f"INSERT INTO dirs_files(Dirs) VALUES(?)", (dir,))
            # inserting files
            for i in range(len(files)):
                for file in files[i]:
                    c.execute(f"INSERT INTO dirs_files(Files) VALUES(?)", (file,))
            conn.commit()
            conn.close()
            print(f"Database Created.Check it out at: {os.path.join(cwd, cachedDir + files_dirsCache)}")
        except sqlite3.OperationalError as e:
            print(e)
        # initialise.FileContentCache(cwd=self.cwd, cachedFile=files_dirsCache, cachedDir=cachedDir)
        initialise.FileContentCache(self, cwd=self.cwd, cachedFile=files_dirsCache, cachedDir=cachedDir)
    def generateCacheFilename(self, file):
        self.file = file
        cacheFilename = ''
        counter = 0
        #unconventional, sorry but this iteration is a quick fix
        for i in range(len(file)):
            if file[i] == "/":
                # counter = counter +1
                cacheFilename = file[i:]
            else:
                pass
        cacheFilename = cacheFilename.replace('/','')
        return cacheFilename

        # @initialise
    def FileContentCache(self, cwd, cachedFile, cachedDir):
        self.cwd = cwd
        self.cachedFile = cachedFile
        self.CachedDir = cachedDir
        FILES = list()
        DIRS = list()
        conn = None
        try:
            conn = sqlite3.connect(cachedFile)
        except sqlite3.Error as e:
            print(e)
        c = conn.cursor()
        # retrieving files from db
        try:
            c.execute('''SELECT Files FROM dirs_files''')
            files = c.fetchall()
            for file in files:
                FILES.append(file)
        except sqlite3.OperationalError as e:
            print('An error occurred whilst executing db commands')
            pass  # find fix
        # retrieving directories
        try:
            c.execute('''SELECT Dirs FROM dirs_files''')
            dirs = c.fetchall()
            for dir in dirs:
                DIRS.append(dir)
        except sqlite3.OperationalError as e:
            print('An error occurred whilst executing db commands')
            pass  # find fix
        # getting true paths of files
        valid_file_paths = initialise.pathFinder(self,fileList=FILES, dirsList=DIRS, cwd=cwd)
        print(valid_file_paths)
        for path in valid_file_paths:
            c.execute('''SELECT CachedPaths FROM dirs_files''')
            c.execute(f"INSERT INTO dirs_files(CachedPaths) VALUES(?)", (path,))
            conn.commit()
        conn.close()
        for file in valid_file_paths:
            lines = list()
            # cacheFilename = f"{cwd}/{cachedDir}{file}_cache.txt"
            cacheFilename =f'{cwd}/{cachedDir}'+str(initialise.generateCacheFilename(self, file=file))+'_cached.txt'
            print(f'CACHEFILENAME:{cacheFilename}')
            # reading content of file
            try:
                with open(file, "r") as f:
                    lines = f.readlines()
                f.close()
                # writing to cache file
                with open(cacheFilename, "w") as fc:
                    for line in lines:
                        fc.write(f"{line}" + "\n")
                fc.close()
            except FileNotFoundError as e:
                print("File does not exist")  # todo: error in pathFinder then.FIX!
                print(file)
                pass
            except UnicodeDecodeError as e:
                # todo: find fix.
                print("Encountered UnicodeDecode error")
                print(file)

    # @initialise
    def pathFinder(self,fileList=None, dirsList=None, cwd=None):
        self.fileList = fileList
        self.dirsList = dirsList
        self.cwd = cwd
        # todo: use for file in filelist
        validPaths = list()
        for i in range(len(fileList)):
            for file in fileList[i]:
                for i in range(len(dirsList)):
                    for dir in dirsList[i]:
                        print(f"CWD:{cwd}")
                        path = f"{cwd}/{dir}/{file}"
                        if os.path.exists(path):  # same base code from previous code
                            validPaths.append(
                                path)  # just broke it into smaller functions check out fileContentCacher in initialiseSCOriginal.py
                        else:
                            pass
        return validPaths








