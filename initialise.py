#!usr/bin/python3
# initialise class
# imports
import os
import sqlite3


class initialise:
    # class variables
    cachedDir = ''
    cachedPath = ''

    def __init__(self):
        # self.cwd = cwd
        self = self

    def initialise(self, cwd):
        self.cwd = cwd + '/'
        # createCache dir
        cachedDir = '.Caches/'
        cachedDir_path = str(self.cwd)+str(cachedDir)
        # checking whether the db dir exists, if not create it
        if os.path.exists(cachedDir_path):
            pass
        else:
            os.mkdir(cachedDir_path)
        # makng cachedb
        db_filename = ('PyGitDB.db')
        db_path = str(cachedDir_path)+ db_filename
        db_file = db_path
        print(db_file)
        if os.path.exists(db_file):
            pass
        else:
            os.system(f'touch %s' % db_file)

        # lists for db commits
        roots = list()
        dirs = list()
        files = list()
        # walking through the dir to harvest data
        for root, dir, file in os.walk(self.cwd, topdown=True):
            roots.append(root)
            dirs.append(dir)
            files.append(file)
        '''checking whether each root is nested'''
        '''if so return single list'''
        # working on roots first
        tmp = initialise.nestedListCheck(roots)
        if tmp == True:
            tmplst = initialise.order_into_a_list(roots)
        elif tmp == False:
            tmplst = roots
        else:
            pass
        roots = tmplst[:]
        tmp *= 0
        tmplst.clear()
        '''checking whether each dir is nested'''
        '''if so return single list'''
        # working on dirs
        tmp = initialise.nestedListCheck(dirs)
        if tmp == True:
            tmplst = initialise.order_into_a_list(dirs)
        elif tmp == False:
            pass
        else:
            pass
        dirs = tmplst[:]
        tmp *= 0
        tmplst.clear()
        '''checking whether each file is nested'''
        '''if so return single list'''
        # working on files
        tmp = initialise.nestedListCheck(files)
        if tmp == True:
            tmplst = initialise.order_into_a_list(files)
        elif tmp == False:
            pass
        else:
            pass
        files = tmplst[:]
        tmp *= 0
        tmplst.clear()
        global conn
        print(db_file)
        conn = sqlite3.connect(db_file)
        try:
            c = conn.cursor()
            # create table
            c.execute('''CREATE TABLE IF NOT EXISTS dirs_files(Roots TEXT, Dirs TEXT, Files TEXT, CachedPaths TEXT)''')
        except sqlite3.Error as e:
            print(e)
        try:
            # inserting lists into db using sqlite3
            for i in range(len(roots)):
                print('Indexing root into db...')
                initialise.progressBar(i, len(roots))
                c.execute(f"INSERT INTO dirs_files(Roots) VALUES(?)", (roots[i],))
            # inserting dirs into db using sqlite3
            for i in range(len(dirs)):
                print('Indexing dirs into db...')
                initialise.progressBar(i, len(dirs))
                c.execute(f"INSERT INTO dirs_files(Dirs) VALUES(?)", (dirs[i],))
            # inserting files into db using sqlite3
            for i in range(len(files)):
                print('Indexing files into db...')
                initialise.progressBar(i, len(files))
                c.execute(f"INSERT INTO dirs_files(Files) VALUES(?)", (files[i],))
            conn.commit()
            conn.close()
            print(f"Database Created.Check it out at: {db_path}")
        except sqlite3.OperationalError as e:
            print(e)
        #caching file content
        initialise.FileContentCache(self, cwd=self.cwd, dbFile=db_file, cached_path=cachedDir_path)

    @staticmethod
    def order_into_a_list(lst):
        tmpLst = list()
        for i in range(len(lst)):
            for item in lst[i]:
                tmpLst.append(item)
        return tmpLst

    @staticmethod
    def nestedListCheck(lst):
        tmplst = lst
        randomItem = 'random'
        for i in range(len(tmplst)):
           try:
               tmplst[i].append(randomItem)
               return True
           except AttributeError as e:
               break
        return False

    # cool progrss bar
    @staticmethod
    def progressBar(current, total, barLength=20):
        percent = float(current) * 100 / total
        arrow = '-' * int(percent / 100 * barLength - 1) + '>'
        spaces = ' ' * (barLength - len(arrow))
        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

    @staticmethod
    def generateCacheFilename(self, file=None):
        self.file = file
        cacheFilename = ''
        counter = 0
        # unconventional, sorry but this iteration is a quick fix
        for i in range(len(file)):
            if file[i] == "/":
                # counter = counter +1
                cacheFilename = file[i:]
            else:
                pass
        cacheFilename = cacheFilename.replace('/', '')
        return cacheFilename

    @staticmethod
    def pathFinder(self, fileList=None, dirsList=None, cwd=None):
        self.fileList = fileList
        self.dirsList = dirsList
        self.cwd = cwd
        valid_paths = list()
        print('Retrieving valid paths...')
        for file in fileList:
            initialise.progressBar(fileList.index(file), len(fileList))
            for dir in dirsList:
                path = f'{cwd}/{dir}/{file}'
                if os.path.exists(path):
                    valid_paths.append(path) # # just broke it into smaller functions check out fileContentCacher in initialiseSCOriginal.py
                else:
                    pass
        return valid_paths

    @staticmethod
    def detupelise(lst):
        tmplst = lst[:]
        tmp2 = list()
        for i in range(len(tmplst)):
            for item in tmplst[i]:
                if item != None:
                    tmp2.append(item)
                else:
                    pass
        return tmp2

    @staticmethod
    def FileContentCache(self, cwd, dbFile, cached_path):
        self.cwd = cwd
        self.dbFile = dbFile
        db_dirs = list()
        db_files= list()
        #Accessing db to retrieving files and directories
        try:
            conn = sqlite3.connect(dbFile)
        except sqlite3.OperationalError as e:
            print('Encountered an error whilst connecting to database\n')
            print(e)
        #retrieving require info
        try:
            c = conn.cursor()
            #retrieving dirs
            c.execute('''SELECT Dirs FROM dirs_files''')
            db_dirs = c.fetchall()
            #retrieving files
            c.execute('''SELECT Files FROM dirs_files''')
            db_files = c.fetchall()
        except sqlite3.OperationalError as e:
            print('Encountered an error whilst connecting to database\n')
            print(e)
        #detupelising the contents of the db(_dirs and _files) contents
        tmplst = list()
        #detupelising dirs
        tmplst = initialise.detupelise(db_dirs)
        db_dirs *=0
        db_dirs = tmplst[:]
        tmplst *= 0
        #detupelising files
        tmplst = initialise.detupelise(db_files)
        db_files *= 0
        db_files = tmplst[:]
        tmplst *= 0
        valid_file_paths = initialise.pathFinder(self, fileList=db_files, dirsList=db_dirs, cwd=self.cwd)
        #inserting valid paths into database
        for path in valid_file_paths:
            print('Indexing valid paths into db...')
            initialise.progressBar(valid_file_paths.index(path), len(valid_file_paths))
            c.execute('''SELECT CachedPaths FROM dirs_files''')
            c.execute('''INSERT INTO dirs_files(CachedPaths) VALUES(?)''', (path,))
            conn.commit()
        conn.close()
        for file_path in valid_file_paths:
            print('CACHING FILE CONTENTS...')
            initialise.progressBar(valid_file_paths.index(file_path), len(valid_file_paths))
            lines = list()
            # cacheFilename = f"{cwd}/{cachedDir}{file}_cache.txt"
            cacheFilename = f'{cached_path}' + str(initialise.generateCacheFilename(self, file=valid_file_paths[valid_file_paths.index(file_path)])) + '_cached.txt'
            # print(f'CACHEFILENAME:{cacheFilename}')
            # print(f'CACHEFILENAME:{cacheFilename}')
            # reading content of file
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                f.close()
                # writing to cache file
                with open(cacheFilename, "w") as fc:
                    for line in lines:
                        fc.write(f"{line}" + "\n")
                fc.close()
            except FileNotFoundError as e:
                print("File does not exist")  # todo: error in pathFinder then.FIX!
                print(file_path)
                pass
            except UnicodeDecodeError as e:
                # todo: find fix.
                print("Encountered UnicodeDecode error")
                print(file_path)

