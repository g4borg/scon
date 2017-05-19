import os, io, sys, logging, time
from PyQt5 import QtGui, QtCore, Qt
from scon.logs.session import LogSessionCollector
from scon.logs import game, combat, chat

class SessionTreeView(Qt.QTreeView):
    def __init__(self, parent):
        super(SessionTreeView, self).__init__(parent)
        self.root_model = Qt.QStandardItemModel()
        self.setModel(self.root_model)
        self.doubleClicked.connect(self.onClickItem)
        self.sessions = None
        self.coll = None
    
    def _populateTree(self, children, parent):
        for child in sorted(children):
            child_item = Qt.QStandardItem(child)
            child_item.setEditable(False)
            #child_item.clicked.connect(self.onClickItem)
            parent.appendRow(child_item)
            if isinstance(children, dict):
                
                if isinstance(children[child], dict):
                    self._populateTree(children[child], child_item)
                
    
    def load_from_directory(self, directory):
        # collect all logs in a directory.
        self.coll = LogSessionCollector(directory)
        # get all unique sessions from this
        self.sessions = self.coll.collect_unique()
        # populate our tree with this dictionary.
        self._populateTree(self.sessions, self.root_model.invisibleRootItem())
        
    def onClickItem (self, signal):
        
        try:
            #print (dir(signal))
            # get the QStandardItem for this entry:
            item = signal.model().itemFromIndex(signal)
            #print (signal.row(), signal.column(), signal.data())
            if not item.parent():
                if item.hasChildren():
                    print ("Already open.")
                    return
                session = self.sessions[signal.data()]
                session.parse_files(['game.log'])
                info_object = Qt.QStandardItem('game.log - %s' % len(session.game_log.lines))
                info_object.setEditable(False)
                item.appendRow(info_object)
                #
                # add all starting events
                for line in session.game_log.lines:
                    if isinstance(line, game.StartingLevel):
                        line.unpack()
                        v = line.values
                        o = Qt.QStandardItem("Level '%s' gametype '%s'" %( v.get('level'),
                                                                       v.get('gametype', '') ))
                        o.setEditable(False)
                        info_object.appendRow(o)
                
                return
                session.parse_files(['combat.log'])
                info_object = Qt.QStandardItem('combat.log - %s' % len(session.combat_log.lines))
                info_object.setEditable(False)
                item.appendRow(info_object)
                #
                session.parse_files(['chat.log'])
                info_object = Qt.QStandardItem('chat.log - %s' % len(session.chat_log.lines))
                info_object.setEditable(False)
                item.appendRow(info_object)
        except:
            import traceback
            traceback.print_exc()

class MainWindow(Qt.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()        
        # setup our main window here.
        
        # setup the directory of your operations
        # see list of all sessions
        # slowly pre scan all sessions
        # if a session is opened, display its contents
        
        # http://stackoverflow.com/questions/27898718/multi-level-qtreeview
        self.tree = SessionTreeView(self)
        layout = Qt.QHBoxLayout(self)
        layout.addWidget(self.tree)
        
        #self.tree.itemClicked.connect(self.onClickItem)
        self.tree.load_from_directory(os.path.join(os.path.expanduser('~'), 'Documents', 'My Games', 'sc'))
        
        # or delayed (not good for debug):
        
        #t = Qt.QTimer()
        #t.singleShot(2, lambda:  self.load_from_directory(
        #          os.path.join(os.path.expanduser('~'),
        #                'Documents', 'My Games', 'sc'))
        #            ,
        #          )
    
    

    
            

def _main():
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    return app.exec_()

def main():
    r = _main()
    try:
        import psutil #@UnresolvedImport
    except ImportError:
        logging.warning('Cannot import PsUtil, terminating without cleaning up threads explicitly.')
        sys.exit(r)
        
    def kill_proc_tree(pid, including_parent=True):    
        parent = psutil.Process(pid)
        if including_parent:
            parent.kill()
    me = os.getpid()
    kill_proc_tree(me)
    sys.exit(r)

if __name__ == "__main__":
    main()