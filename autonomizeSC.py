#autonomise
#imports
import os
import sqlite3
import sys
import difflib
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from initialise import  initialise
class autonomize:
    def __init__(self):
        self = self
    def autonomize(self, cwd):
        #make sure the user knows that initialise script must be run first
        print('To proceed, ensure you have run the initialise module before'
              '\nAfterwards you can comment it out'
              '\nEXAMPLE: from PyGit import initialise'
              '\ninitialise.initialise().initialise(cwd=os.path.dirname(os.path.realpath(__file__)))'
              '\n YOU CAN CHOOSE TO COMMENT IT OUT LATER'
              '\n'
              '\nHAVE ALL THESE BEEN SATISFIED?')
        opt = str(input('Y/N: '))
        if opt.lower() == "y":
            pass
        elif opt.lower() == "n":
            # print('PLEASE SATISFY IT!')
            print('WORKING ON IT!')
            initialise.initialise(self, cwd=os.path.dirname(os.path.realpath(__file__)))
            print('DONE.')
        else:
            print('UNKNOWN CHOICE!')
        """START OF AUTONOMIZE"""
        #lists declarations
        filenamesLst = list()
        dirsLst = list()
        rootsLst = list()
        updatedFilnames = list()
        updatedDirs = list()
        updatedRoots = list()
        FileChangesLst = list()
        DirChangesLst = list()
        RootChangesLst = list()
        FilesReview = list() #this list stores all the filenames which have not changed.Their contents will be reviewd with the cached ones.

        #updating all update lists
        for root, dir, file in os.walk(cwd, topdown=False):
            updatedRoots.append(root)
            updatedDirs.append(dir)
            updatedFilnames.append(file)
        #connecting to database
        cachedDir = "Caches/"
        dbfile = 'F_DCache.db'
        db = f'{cwd}/{cachedDir}{dbfile}'
        # print(db)
        #todo: put try except block ftom initialise code here
        # try:
        #     conn = sqlite3.connect(db)
        #     c = conn.cursor()
        # except sqlite3.Error as e:
        #     print('Encountered a problem whilst connecting to db.')
        conn = sqlite3.connect(db)
        c = conn.cursor()
        #retrieving original file lists
        c.execute('''SELECT Files FROM dirs_files''')
        #working on the tuples received from the db
        tmplst = c.fetchall()
        for i in range(len(tmplst)):
            for j in range(len(tmplst[i])):
                if tmplst[i][j] != None:
                    filenamesLst.append(tmplst[i][j])
                else:
                    pass
        del tmplst[:] #can also use tmplst.clear()
        # print(f"FILENAMELST:{filenamesLst}")
        # print(f'UPDATEDFILENAMES: {updatedFilnames}')
        for i in range(len(updatedFilnames)):
            for filename in updatedFilnames[i]:
                #returns tuple so retriving tuple objects which are not None
                # for j in range(len(filename)):
                if filename != None:
                    if filename not in filenamesLst:
                        FileChangesLst.append(filename)
                    else:
                        FilesReview.append(filename)
                else:
                    pass
        #todo:cros check folder names
        #retrieving original folders
        c.execute('''SELECT Dirs FROM dirs_files''')
        tmplst = c.fetchall()
        for i in range(len(tmplst)):
            for j in range(len(tmplst[i])):
                if tmplst[i][j] !=None:
                    dirsLst.append(tmplst[i][j])
                else:
                    pass
        tmplst[:]
        originalDir = list()
        for i in range(len(updatedDirs)):
            for dir in updatedDirs[i]:
                #returns tuple.Want to append just the contents
                if dir != None:
                    if dir not in dirsLst:
                        DirChangesLst.append(dir)
                    else:
                        originalDir.append(dir)
                else:
                    pass

        #todo: cross check root names
        c.execute('''SELECT Roots FROM dirs_files''')
        rootsLst = c.fetchall()
        for root in updatedRoots:
            if root not in rootsLst:
                RootChangesLst.append(root)
            else:
                pass
        #todo:function to compare contents of files
        #checking the contents of files
        valid_file_paths = initialise.pathFinder(self, fileList=FilesReview, dirsList=originalDir, cwd=cwd)
        # print(f"FILENAMELISTS:{FilesReview}")
        for i in range(len(valid_file_paths)):
            autonomize.compare(self, filename=valid_file_paths[i], cacheDIR=cachedDir)
    def compare(self, filename, cacheDIR):
        self.filename = filename
        self.cacheDIR = cacheDIR
        #working with tuple objects so need only specific items
        cache_of_file = f'{filename}_cached.txt'
        print(f'CACHEFILE:{cache_of_file}')
        file_lines = list()
        cache_line = list()
        print(f'FILENAME:{filename}')
        with open(filename, 'r') as f:
            file_lines = f.readlines()
        f.close()
        with open(cache_of_file, 'r') as f:
            cache_line = f.readlines()
        f.close()
        print(f'DIFFERENCES FOUND BETWEEN {filename} and {cache_of_file}')
        sys.stdout.writelines(difflib.context_diff(file_lines, cache_line))


