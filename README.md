![Image of PyGit Logo](https://github.com/malgulam/PyGit/blob/master/PyGitLogo.png) 
# PyGit
## Python Git VC Tool.
### This package acts as a version control tool that helps python developers to create,edit,etc from within the program itself.

```python
import PyGit
from PyGit import initialise, autonomize
!#/usr/python3
def something():
    #autonomize.autonomize().autonomize(cwd=os.path.dirname(os.path.realpath(__file__)))
    #initialise.initialise().initialise(cwd=os.path.dirname(os.path.realpath(__file__)))
something()
```

**NB:**
 - Use initialise script on first run to cache all required files, folders and roots into sqlite3 db.

 - Fix 'touch command' in 'initialise.py' line 38 

 - Create  an sqlie3 condition to avoid caching files, dirs, roots, valid paths which  have already been cached in      F_DCache.db again.

 - Contribute!

*Check out pypi @druzgeorge @agulam-coco*



**Much contribution will be needed.Thanks in advance. :]**
