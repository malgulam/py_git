#autonomise
#imports
import os
import sqlite3
import sys
import difflib
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from initialise import  initialise
# from initialise import valid
class autonomize:
    def __init__(self):
        self = self
    @staticmethod
    def compare(self, filename, cacheDIR):
        self.filename = filename
        self.cacheDIR = cacheDIR
        # working with tuple objects so need only specific items
        cache_of_file = initialise.generateCacheFilename(self, file=filename)
        cache_of_file_path = f'{self.cwd}/{self.cacheDIR}{cache_of_file}_cached.txt'
        print(f'CACHEFILE:{cache_of_file_path}')
        self.file_lines = list()
        self.cache_line = list()
        print(f'FILENAME:{filename}')
        with open(filename, 'r') as f:
            self.file_lines = f.readlines()
        f.close()
        with open(cache_of_file_path, 'r') as f:
            self.cache_line = f.readlines()
        f.close()
        print(f'DIFFERENCES FOUND BETWEEN {filename} and {cache_of_file_path}')
        sys.stdout.writelines(difflib.context_diff(self.file_lines, self.cache_line))

    def autonomize(self, cwd):
        self.cwd = cwd
        # START OF PROGRAM
        #run autonomize
        #database declarations
        cachedDir = "Caches/"
        dbfile = 'F_DCache.db'
        db = f'{cwd}/{cachedDir}{dbfile}'
        try:
            while True:
                # lists declarations
                filenamesLst = list()
                dirsLst = list()
                rootsLst = list()
                updatedFilnames = list()
                updatedDirs = list()
                updatedRoots = list()
                FileChangesLst = list()
                DirChangesLst = list()
                RootChangesLst = list()
                FilesReview = list()  # this list stores all the filenames which have not changed.Their contents will be reviewd with the cached ones.

                #updating all update lists
                for root, dir, file in os.walk(cwd, topdown=False):
                    updatedRoots.append(root)
                    updatedDirs.append(dir)
                    updatedFilnames.append(file)
                #connecting to db
                conn = sqlite3.connect(db)
                c = conn.cursor()
                #RETRIEVING ORIGINAL FILES FROM DB
                c.execute('''SELECT Files FROM dirs_files''')
                tmplst = c.fetchall()
                for i in range(len(tmplst)):
                    for j in range(len(tmplst[i])):
                        if tmplst[i][j] != None:
                            filenamesLst.append(tmplst[i][j])
                        else:
                            pass
                del tmplst[:]  # can also use tmplst.clear()
                # print(f"FILENAMELST:{filenamesLst}")
                # print(f'UPDATEDFILENAMES: {updatedFilnames}')
                for i in range(len(updatedFilnames)):
                    for filename in updatedFilnames[i]:
                        # returns tuple so retriving tuple objects which are not None
                        # for j in range(len(filename)):
                        if filename != None:
                            if filename not in filenamesLst:
                                FileChangesLst.append(filename)
                            else:
                                FilesReview.append(filename)
                        else:
                            pass

                # retrieving original folders
                c.execute('''SELECT Dirs FROM dirs_files''')
                tmplst = c.fetchall()
                for i in range(len(tmplst)):
                    for j in range(len(tmplst[i])):
                        if tmplst[i][j] != None:
                            dirsLst.append(tmplst[i][j])
                        else:
                            pass
                tmplst[:]
                originalDir = list()
                for i in range(len(updatedDirs)):
                    for dir in updatedDirs[i]:
                        # returns tuple.Want to append just the contents
                        if dir != None:
                            if dir not in dirsLst:
                                DirChangesLst.append(dir)
                            else:
                                originalDir.append(dir)
                        else:
                            pass

                #Retrieving roots from db
                c.execute('''SELECT Roots FROM dirs_files''')
                rootsLst = c.fetchall()
                for root in updatedRoots:
                    if root not in rootsLst:
                        RootChangesLst.append(root)
                    else:
                        pass
                # checking the contents of files
                print(f'FILESREVIEW:{FilesReview}')
                valid_file_paths = initialise.pathFinder(self, fileList=FilesReview, dirsList=originalDir, cwd=cwd)
                for path in valid_file_paths:
                    try:
                        autonomize.compare(self, filename=path,cacheDIR=cachedDir)
                    except FileNotFoundError:
                        print(f'File not found.Hm!: {path}')
                        break
        except sqlite3.OperationalError as e:
            print('Seems there\'s no db present')
            time.sleep(0.5)

            print('To proceed, ensure you have run the initialise module before'
              '\nAfterwards you can comment it out'
              '\nEXAMPLE: from PyGit import initialise'
              '\ninitialise.initialise().initialise(cwd=os.path.dirname(os.path.realpath(__file__)))'
              '\n YOU CAN CHOOSE TO COMMENT IT OUT LATER'
              '\n'
              '\nHAVE ALL THESE BEEN SATISFIED?')
            print('\n\n\n')
            print('Want to create db? Y\\N: ', end='')
            opt =  str(input())
            if opt.lower() == 'y':
                initialise.initialise(self, cwd=os.getcwd())
                # initialise.__init__(self=self, cwd=os.getcwd()).initialise()
                print('DONE!\nRestart the compiler sequence.')
            elif opt.lower() == 'n':
                print('ABORTED!')
            else:
                print('UNKNOWN COMMAND')

