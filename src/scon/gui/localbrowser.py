import os, logging
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from treeview import TreeViewModel, Node
from django.test import Client

class DebugPage(QtWebKit.QWebPage):
    def sayMyName(self):
        return 'DebugPage'

class LocalWebView(QtWebKit.QWebView):
    def __init__(self, *args, **kwargs):
        basedir = kwargs.pop('basedir', None)
        QtWebKit.QWebView.__init__(self, *args, **kwargs)
        oldManager = self.page().networkAccessManager()
        self.setPage(DebugPage())
        self.page().setNetworkAccessManager(LocalNetworkAccessManager(self, basedir))
    
    def set_basedir(self, basedir):
        self.page().setNetworkAccessManager(LocalNetworkAccessManager(self, basedir))    

class LocalNetworkAccessManager(QtNetwork.QNetworkAccessManager):
    USE_NETWORK = False
    def __init__(self, parent=None, basedir=None):
        QtNetwork.QNetworkAccessManager.__init__(self, parent=None)
        if not basedir:
            # take current dir as basedir.
            self.basedir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.basedir = basedir

    def createRequest(self, operation, request, data):
        scheme = request.url().scheme()
        if scheme != 'page' and scheme != 'image':
            if self.USE_NETWORK:
                return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        elif scheme == 'page':
            if operation == self.GetOperation:
                # Handle page:// URLs separately by creating custom
                # QNetworkReply objects.
                reply = PageReply(self, request.url(), self.GetOperation)
                #print('here')
                #print reply
                return reply
            elif operation == self.PostOperation:
                #print data.readAll()
                #print request
                reply = PageReply(self, request.url(), self.PostOperation)
                return reply
        elif scheme == 'image':
            if operation == self.GetOperation:
                return ImageReply(self, request.url(), self.GetOperation, self.basedir)
        else:
            if self.USE_NETWORK:
                return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return NoNetworkReply(self, request.url(), self.GetOperation)

class BasePageReply(QtNetwork.QNetworkReply):
    content_type = 'text/html; charset=utf-8'
    def __init__(self, parent, url, operation):
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.content = self.initialize_content(url, operation)
        self.offset = 0
        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, self.get_content_type())
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL('readyRead()'))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL('finished()'))
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
    
    def get_content_type(self):
        return self.content_type
    
    def initialize_content(self, url, operation):        
        return '''
            <html>
            <head><title>Test</title></head>
            <body><form method="POST" action=".">
            <img src="image:///scon/conflict-logo.png">
            <input type="text" name="a"></input>
            <input type="text" name="b"></input>
            <button class="submit">Submit</button></form></body>
            </html>
        '''

    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) - self.offset + QtNetwork.QNetworkReply.bytesAvailable(self)

    def isSequential(self):
        return True

    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data

class PageReply(BasePageReply):
    def initialize_content(self, url, operation):
        c = Client()
        print(("Response for %s, method %s" % (url.path(), operation)))
        if operation == LocalNetworkAccessManager.GetOperation:
            response = c.get(str(url.path()), )
        elif operation == LocalNetworkAccessManager.PostOperation:
            response = c.post(str(url.path()))
        # response code
        print(("Response Status: %s" % response.status_code))
        # note: on a 404, we might need to trigger file response.
        return response.content

class NoNetworkReply(BasePageReply):
    def initialize_content(self, url, operation):
        return '''
            <html>
            <head><title>No Network Access.</title></head>
            <body>
            Internal access to the network has been disabled.
            </body>
            </html>
        '''

class ImageReply(BasePageReply):
    content_type = 'image/png'
    def __init__(self, parent, url, operation, basedir):
        self.basedir = basedir
        BasePageReply.__init__(self, parent, url, operation)
        
    def initialize_content(self, url, operation):
        path = os.path.join(self.basedir, str(url.path()).lstrip('/'))
        if not os.path.exists(path):
            logging.error('Image does not exist: %s' % path)
            return ''
        h = url.host()
        try:
            f = open(path, 'rb')
            return f.read()
        finally:
            f.close()
        