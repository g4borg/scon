
import logging, os
try:
    from django.conf import settings
except:
    logging.error('Django Settings could not be loaded. Maybe Django has not been initialized?')
    settings = None

class FolderLibrary(object):
    def __init__(self, folders=None):
        self._folders = {}
        try:
            if settings:
                self.folders.update( getattr(settings, 'DEJAQT_DIRS', {}) )
        except:
            logging.error('DEJAQT_DIRS in django settings is corrupt.')
        if folders:
            # no try here: if this fails, you got yourself a programming error.
            self.folders.update(folders)
        self._keys = []
        self.build_keycache()
    
    def get_folders(self):
        return self._folders
    
    def set_folders(self, folders):
        self._folders = folders
        self.build_keycache()
    folders = property(get_folders, set_folders)
    
    def build_keycache(self):
        self._keys = self._folders.keys()
        self._keys.sort(key=lambda item: (-len(item), item))
    
    def add_folder(self, url, folder):
        if not url:
            url = ''
        self._folders[url] = folder
        self.build_keycache()
    
    def match(self, url):
        # run down our keycache, first match wins.
        for key in self._keys:
            if url.startswith(key):
                return key
    
    def matched_folder(self, url):
        m = self.match(url)
        if m is not None:
            real_folder = self._folders[m]
            print m
            print url
            print url[len(m):]
            print os.path.split(real_folder)
            print os.path.split(url)
            return real_folder
        
    def print_folders(self):
        print '{'
        for k in self._keys:
            print "'%s': '%s'" % (k, self._folders[k])
        print '}'
    

if __name__ == "__main__":
    # test this:
    f = FolderLibrary({'abc/dab/': 'c:/dab',
                       'abc': 'd:/abc',
                       'abc/dab/tmp': '/tmp',
                       'uiuiui': 'x:/',
                       'abc/vul/no': 'x:/2',
                       'abc/vul': 'x:/3',
                       'abc/vul/yes': 'x:/1',
                       })
    f.add_folder('abc/dub/', 'c:/dubdub')
    f.print_folders()
    
    print f.matched_folder('abc/dab/okokok/hurnkint.pdf')
    