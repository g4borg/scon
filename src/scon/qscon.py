"""
    Main Entry Point / Exe File for QScon, the main log handler / monitor / manager app for log files.
    
"""
import os, sys, logging
import sys
import urllib2
from PyQt4 import QtCore, QtGui
from monitor import SconMonitor
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


class SconMonitorThread(QtCore.QThread):
    updated = pyqtSignal(str, list)
    created = pyqtSignal(str, bool)
    
    def __init__(self, path):
        QtCore.QThread.__init__(self)
        self.path = path
    
    def notify(self, filename, lines):
        self.updated.emit(filename, lines)
        #self.mainwindow.notify_filelines(filename, lines)
        #self.list_widget.addItem('%s\n%s' % (filename, ''.join(lines)))
    
    def notify_event(self, event_type, data):
        if event_type == 'created':
            self.created.emit(data['src'], data['is_dir'])

    def run(self):
        monitor = SconMonitor(self.path, notifier=self)
        #self.list_widget.addItem('Starting to monitor: %s' % self.path)
        monitor.run()

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()        
        self.tab_list = QtGui.QTabWidget()
        self.tabs = {}
        self.button = QtGui.QPushButton("Start")
        self.button.clicked.connect(self.start_monitor)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.tab_list)
        self.setLayout(layout)
    
    
    def notify_filelines(self, filename, lines):
        if filename not in self.tabs.keys():
            new_tab = QtGui.QWidget()
            new_tab.list_widget = QtGui.QListWidget()
            layout = QtGui.QVBoxLayout(new_tab)
            layout.addWidget(new_tab.list_widget)
            self.tabs[filename] = new_tab
            self.tab_list.addTab(new_tab, "%s" % os.path.split(str(filename))[-1])
        self.tabs[filename].list_widget.addItem(''.join(lines)[:-1])
    
    def notify_created(self, filename, is_directory):
        if is_directory:
            print "Created Directory %s" % filename
        else:
            print "Created File %s" % filename

    def start_monitor(self):
        self.button.setDisabled(True)
        paths = [os.path.join(os.path.expanduser('~'),'Documents','My Games','StarConflict','logs'),
                 ]
        self.threads = []
        for path in paths:
            athread = SconMonitorThread(path)
            athread.updated.connect(self.notify_filelines)
            athread.created.connect(self.notify_created)
            self.threads.append(athread)
            athread.start()

########################################################################

def _main():
    app = QtGui.QApplication(sys.argv)
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
    