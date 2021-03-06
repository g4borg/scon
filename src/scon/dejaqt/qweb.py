"""
    Qt WebKit Browser for local access to internal Django Views.
"""
import os, logging
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from django.test import Client
from .folders import FolderLibrary
from django.http.request import QueryDict
from urllib.parse import urlparse, parse_qs
import cgi
from io import BytesIO
from django.http.multipartparser import MultiPartParser

class DebugPage(QtWebKit.QWebPage):
    def sayMyName(self):
        return 'DebugPage'

class DejaWebView(QtWebKit.QWebView):
    '''
        Optional: 
          * folders: FolderLibrary() Instance.
          * page: Initialized QWebPage instance for initial page (default DebugPage())
    '''
    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', FolderLibrary())
        page = kwargs.pop('page', DebugPage())
        QtWebKit.QWebView.__init__(self, *args, **kwargs)
        #self.oldManager = self.page().networkAccessManager()
        self.setPage(page)
        self.page().setNetworkAccessManager(DejaNetworkAccessManager(self))
        self.client = Client()
        #self.client.login(username='admin', password='admin')

class DejaNetworkAccessManager(QtNetwork.QNetworkAccessManager):
    '''
        The Deja Network Access Manager provides access to two new protocols:
        - page:/// tries to resolve a page internally via a django test client.
        - res:/// direct access to a resource.
        
        USE_NETWORK delegates to other network access manager protocols, if False, it will not
        allow any requests outside these two protocols 
        (hopefully disabling network access for your internal browser)
        
        Note, if page does not find the page, a res:/// attempt is made automatically.
        This has to be expanded!
        
        Note2: not sure if cookies and sessions will work this way!
    '''
    USE_NETWORK = False
    def __init__(self, parent=None):
        QtNetwork.QNetworkAccessManager.__init__(self, parent=parent)
        if parent:
            self.folders = getattr(parent, 'folders', FolderLibrary())
        
    def createRequest(self, operation, request, data):
        scheme = request.url().scheme()
        if scheme != 'page' and scheme != 'res':
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
                reply = PageReply(self, request.url(), self.PostOperation, request, data)
                return reply
        elif scheme == 'res':
            if operation == self.GetOperation:
                return ResourceReply(self, request.url(), self.GetOperation)
        else:
            if self.USE_NETWORK:
                return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        return NoNetworkReply(self, request.url(), self.GetOperation)

class BasePageReply(QtNetwork.QNetworkReply):
    content_type = 'text/html; charset=utf-8'
    def __init__(self, parent, url, operation, request=None, data=None):
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.data = data
        self.request = request
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
            <head><title>Empty Page</title></head>
            <body>This is an empty page. If you see this, you need to subclass BasePageReply.</body>
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

class ResourceReply(BasePageReply):
    content_type = 'image/png'
    
    def determine_content_type(self, path):
        return self.content_type
        
    def initialize_content(self, url, operation):
        # determine folder:
        path = str(url.path()).lstrip('/')
        folders = getattr(self.parent(), 'folders')
        if folders:
            path = folders.matched_folder(path)
            if path:
                if os.path.exists(path):
                    try:
                        f = open(path, 'rb')
                        return f.read()
                    finally:
                        f.close()
                else:
                    logging.warning('Path does not exist: %s' % path)
            else:
                logging.error('Containing Folder not found for %s' % path)
        else:
            logging.error('Configuration Error: No Folders found.')
        return ''
    
class PageReply(ResourceReply):
    content_type = 'text/html'
    
    def initialize_content(self, url, operation):
        try:
            c = self.parent().parent().client
        except:
            logging.error('Internal HTTP Client not found. Creating new.')
            c = Client()
        logging.info( "Response for %s, method %s" % (url.path(), operation) )
        if operation == DejaNetworkAccessManager.GetOperation:
            response = c.get(str(url.path()), follow=True )
        elif operation == DejaNetworkAccessManager.PostOperation:
            ct = str(self.request.rawHeader('Content-Type'))
            cl = str(self.request.rawHeader('Content-Length'))
            s = str(self.data.readAll())
            if ct.startswith('multipart/form-data'):
                # multipart parsing
                logging.error('Multipart Parsing Try...')
                b = BytesIO(s)
                q, files = MultiPartParser({'CONTENT_TYPE': ct,
                                 'CONTENT_LENGTH': cl,
                                 },
                                b,
                                []).parse()
                response = c.post(str(url.path()), q, follow=True)
            else:
                # assume post data.
                q = QueryDict( s )
                response = c.post(str(url.path()), q, follow=True)
        self.content_type = response.get('Content-Type', self.content_type)
        # response code
        #print "Response Status: %s" % response.status_code
        # note: on a 404, we might need to trigger file response.
        if response.status_code == 404:
            return ResourceReply.initialize_content(self, url, DejaNetworkAccessManager.GetOperation)
        if hasattr(response, 'streaming_content'):
            return ''.join(response.streaming_content)
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

