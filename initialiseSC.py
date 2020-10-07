import os
import sqlite3
from datetime import date
import difflib
from pathlib import Path

class initialise:
    #cached dir will be hidden by default
    caches_dir = ''
    caches_dir_path = ''
    def __init__(self):
        pass
    '''Know most of methods need to be classmethod.Need to keep things simple for now.Change later.'''
    def initialise(self, cwd, current_file):
        self.current_file = current_file
        self.cwd = cwd + '/'
        #create cache dir
        caches_dir = '.Caches/'
        caches_dir_path = str(self.cwd)+str(caches_dir)
        #check whether the db exists, if not create it
        if not os.path.exists(caches_dir_path):
            initialise.safe_mkdir(caches_dir_path)
        db_file = ('PyGitDB.db')
        db_file_path = str(caches_dir_path)+db_file
        #check whether db file exists.If not create it.
        if not os.path.exists(db_file):
            os.system(f'touch %s' %db_file_path)
        #working filename of file importing pygit.initialise()
        print('cwd:', self.cwd)
        current_filename = initialise.find_filename_(self.cwd)
        #create database table for file and version
        #File DB SCHEMA
        #ID|File|Version|Date Created|
        #|1| main.py| main.py_ver1_cache.txt| sep 14 2020|
        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()
        print('current filename:',current_file)
        database_current_file_name = Path(current_file).stem
        print('database_current_filename',database_current_file_name)
        # c.execute(f'''CREATE TABLE IF NOT EXISTS {current_file}(id INTEGER, FILE TEXT,VERSION INTEGER, DATE_CREATED TEXT)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS file(id INTEGER,File TEXT, VERSION INTEGER, DATE_CREATED TEXT)''')
        conn.commit()
        #retrieving data from the column {current_filename} to see if null
        c.execute(f'''SELECT File FROM file ORDER BY id DESC LIMIT 1;''')
        files = c.fetchall()
        #if files is empty that means this is the first run
        #file version
        last_version_num = 0
        if not files:
            last_version_num += 0
        #set version  number by default
        c.execute(f'''SELECT id FROM file ORDER BY id DESC LIMIT 1;''')
        last_version_num = c.fetchone()
        if last_version_num !=None:
            pass
        last_version_num = 0
        #working on the cache file
        #todo: workout easier  how to ask user for file name self.file_base_path using the Path(__file__).name
        cache_filename_ = ''
        initialise.FileContentCache(cwd=self.cwd, dbFile= db_file_path, caches_path = caches_dir_path,file=current_file, last_ver_num =last_version_num)

        #checking if files is null

        #todo: write file versions to txt HEADS
        # HEADS_path = str(self.cwd) + 'HEADS.txt'
        # with open(HEADS_path, 'w') as HEADS:
        #
        #     HEADS.write()
        #todo: write contents of file to _txt file
        #todo: increment the id of the cache file
    @staticmethod
    def progressBar(current, total, barLength=20):
        percent = float(current) * 100 / total
        arrow = '-' * int(percent / 100 * barLength - 1) + '>'
        spaces = ' ' * (barLength - len(arrow))
        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
    @staticmethod
    def safe_mkdir(dir):
        if os.path.exists(dir):
            return
        os.mkdir(dir)
    @staticmethod
    def find_filename_(file):
        slash_count = 0
        for i in range(len(file)):
            if not file[i] == '/':
                pass
            slash_count += 1
        return file[slash_count:]
    @staticmethod
    def generate_cache_filename(file=None):
        cache_filename = str(initialise.find_filename_(file))
        return cache_filename
    @staticmethod
    def analyse_content(original_filename, cache_filename):
        original_file_lines = list()
        cache_file_lines = list()
        with open(original_filename, 'r') as f:
            original_file_lines = f.readlines()
        f.close()
        with open(cache_filename, 'r') as f:
            cache_file_lines = f.readlines()
        f.close()
        d = difflib.Differ()
        diffs = [x for x in d.compare(original_file_lines, cache_file_lines) if x[0] in ('+', '-')]
        if diffs:
            #all rows with changes
            print(diffs)
        else:
            print('No changes.')
    @staticmethod
    def FileContentCache(cwd, dbFile, caches_path,file, last_ver_num):
        #user prompts
        print(f'Writing Cache of {file}')
        for i in range(101):
            initialise.progressBar(i, 101)
        #retrieving today's date
        tday_date = date.today()
        try:
            conn = sqlite3.connect(dbFile)
        except sqlite3.OperationalError as e:
            print('Encountered an error whilst connecting to database\n')
            print(e)
        #cache_file_name
        print('lastver',last_ver_num)
        latest_version = last_ver_num + 1
        cache_filename = f'{caches_path}' + str(initialise.generate_cache_filename(file=file)) + str(
            latest_version) + '_cached.txt'
        try:
            c = conn.cursor()
            #todo: insert  the cachefilename here as File version
            lines = list()
            with open(file, 'r') as f:
                lines = f.readlines()
            f.close()
            #writing to cache file
            with open(cache_filename,'w') as fc:
                for line in lines:
                    fc.write(f"{line}\n")
            fc.close()
            totalData = [latest_version, cache_filename, latest_version, tday_date]
            c.execute(f'''INSERT INTO file(id,File , VERSION , DATE_CREATED ) VALUES (?,?,?,?)''', totalData[:])
            conn.commit()
            print('done')
        except sqlite3.OperationalError as e:
            print('Encountered an error whilst connecting to database\n')
            print(e)

        initialise.analyse_content(original_filename=file, cache_filename = cache_filename)
