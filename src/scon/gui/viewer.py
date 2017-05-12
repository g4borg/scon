# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Viewer - starts a webbrowser which is coupled to a local renderer
    
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'scon.dj.settings' 
#from django.core.management  import setup_environ
#from scon.dj import settings
#setup_environ(settings)
import sys
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from scon.dejaqt.folders import FolderLibrary
from scon.dejaqt.qweb import DejaWebView
from .treeview import TreeViewModel, Node

class MenuTree(QtGui.QTreeView):
    def __init__(self, *args, **kwargs):
        QtGui.QTreeView.__init__(self, *args, **kwargs)
        self.test_tree()
    
    def test_tree(self):
        self.rootNode = Node("Rootdir")
        model = TreeViewModel(self.rootNode)
        self.setModel(model)
        self.rootNode.addChild(Node('Hey'))
         

class Browser(QtGui.QMainWindow):

    def __init__(self):
        """
            Initialize the browser GUI and connect the events
        """

        QtGui.QMainWindow.__init__(self)
        self.resize(860,600)
        self.centralwidget = QtGui.QWidget(self)

        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(1)

        self.frame = QtGui.QFrame(self.centralwidget)

        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.tb_url = QtGui.QLineEdit(self.frame)
        self.bt_back = QtGui.QPushButton(self.frame)
        self.bt_ahead = QtGui.QPushButton(self.frame)

        self.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
        self.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))

        self.horizontalLayout.addWidget(self.bt_back)
        self.horizontalLayout.addWidget(self.bt_ahead)
        self.horizontalLayout.addWidget(self.tb_url)
        self.gridLayout.addLayout(self.horizontalLayout)
        
        self.horizontalMainLayout = QtGui.QHBoxLayout()
        self.gridLayout.addLayout(self.horizontalMainLayout)
        #
        #self.menu = MenuTree()
        self.html = DejaWebView(folders=FolderLibrary({'':
                                                        'D:/work/workspace/scon/src/scon/dj/scon/media/'})
                                 )
        #self.horizontalMainLayout.addWidget(self.menu)
        self.horizontalMainLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)

        self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
        self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
        self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)

        self.tb_url.setText('/crafting/forum')
        
        self.browse()

    def browse(self):
        """
            Make a web browse on a specific url and show the page on the
            Webview widget.
        """

        url = self.tb_url.text() if self.tb_url.text() else 'page:///'
        if not str(url).startswith('page://'):
            url = 'page://' + url
        self.html.load(QtCore.QUrl(url))
        #self.html.setHtml(self.serve())
        
        #self.html.load(QtCore.QUrl('page:///crafting/forum/'))
        self.html.show()
        
    def serve(self, what=None):
        return "<html><body><h1>It works!</h1></body></html>"

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    main = Browser()
    main.show()
    sys.exit(app.exec_())
    
