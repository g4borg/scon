# -*- coding: utf-8 -*-
from logs.base import Log, L_WARNING, Stacktrace
import re
"""
Responsible for Chat Log.

ColorChart:
between 33-33-33 and FF-33 FF-33 FF-33

"""

class ChatLog(Log):
    __slots__ = ['matcher', 'trash', '_match_id', 'values']
    
    @classmethod
    def is_handler(cls, log):
        if log.get('logtype', None) == 'CHAT':
            return cls._is_handler(log)
        return False
    
    @classmethod
    def _is_handler(cls, log):
        return False
    
    def __init__(self, values=None):
        self.values = values or {}
        self.reviewed = False
    
    def unpack(self, force=False):
        if self.reviewed and not force:
            return True
        self._match_id = None
        # unpacks the data from the values.
        if hasattr(self, 'matcher') and self.matcher:
            matchers = self.matcher
            if not isinstance(matchers, list):
                matchers = [matchers,]
            for i, matcher in enumerate(matchers):
                m = matcher.match(self.values.get('log', ''))
                if m:
                    self.values.update(m.groupdict())
                    self._match_id = i
                    self.reviewed = True
                    return True
        # unknown?
        self.trash = True
    
    def explain(self):
        ''' returns a String readable by humans explaining this Log '''
        return self.values.get('log', 'Unknown Chat Log')
    
    def clean(self):
        if 'log' in self.values.keys():
            del self.values['log']

class SystemMessage(ChatLog):
    matcher = re.compile(r"^<\s+SYSTEM>\s(?P<message>.*)")
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('<          SYSTEM>'):
            return True
        return False
    
    def explain(self):
        return '[SYSTEM]: %(message)s' % self.values
    
    def append(self, something):
        ''' System Messages accept appends '''
        if 'message' in self.values.keys():
            self.values['message'] = '%s\n%s' % (self.values['message'], something)
            return True

    

class PrivateMessageReceived(ChatLog):
    matcher = re.compile(r"^<\s\s\s\sPRIVATE From>\[\s*(?P<nickname>[^\]]+)\]\s(?P<message>.*)")
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('<    PRIVATE From>'):
            return True
        return False
    
    def explain(self):
        return '[From %(nickname)s]: %(message)s' % self.values
    
    def append(self, something):
        ''' Private Messages accept appends '''
        if 'message' in self.values.keys():
            self.values['message'] = '%s\n%s' % (self.values['message'], something)
            return True

class PrivateMessageSent(ChatLog):
    matcher = re.compile(r"^<\s\s\s\sPRIVATE To\s\s>\[\s*(?P<nickname>[^\]]+)\]\s(?P<message>.*)")
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('<    PRIVATE To  >'):
            return True
        return False
    
    def explain(self):
        return '[To %(nickname)s]: %(message)s' % self.values
    
    def append(self, something):
        ''' Private Messages accept appends '''
        if 'message' in self.values.keys():
            self.values['message'] = '%s\n%s' % (self.values['message'], something)
            return True

class ChatMessage(ChatLog):
    matcher = re.compile(r"^<\s*#(?P<channel>[^>]+)>\[\s*(?P<nickname>[^\]]+)\]\s(?P<message>.*)")
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('<'):
            return True
        return False
    
    def explain(self):
        return '[%(channel)s] <%(nickname)s>: %(message)s' % self.values
    
    def append(self, something):
        ''' ChatMessages accept appends '''
        if not 'message' in self.values.keys():
            print "Missing message? %s" % self.values
            self.values['message'] = ''    
        self.values['message'] = '%s\n%s' % (self.values['message'], something)
        return True 

class ChatJoinChannel(ChatLog):
    matcher = re.compile(r"^Join\schannel\s<\s*#(?P<channel>[^>]+)>")

    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('Join channel'):
            return True
        return False
    
    def explain(self):
        return '[joined %(channel)s]' % self.values

class ChatLeaveChannel(ChatLog):
    matcher = re.compile(r"^Leave\schannel\s<\s*#(?P<channel>[^>]+)>")
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('Leave channel'):
            return True
        return False

    def explain(self):
        return '[left %(channel)s]' % self.values


class ChatServerConnect(ChatLog):
    # 00:12:47.668     CHAT| Connection to chat-server established
    matcher = []
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('Connection to'):
            return True
        return False
    
    def unpack(self, force=False):
        self.reviewed = True
        return True
    
    def explain(self):
        return '[connected]'


class ChatServerDisconnect(ChatLog):
    # 00:53:03.738     CHAT| Disconnect form chat-server (reason 0)
    matcher = []
    
    @classmethod
    def _is_handler(cls, log):
        if log.get('log', '').lstrip().startswith('Disconnect'):
            return True
        return False
    
    def unpack(self, force=False):
        self.reviewed = True
        return True

    def explain(self):
        return '[disconnected]'
    
CHAT_LOGS = [
        SystemMessage,
        PrivateMessageReceived,
        PrivateMessageSent,
        ChatMessage, # private messages need to be before chatmessage.
        ChatServerConnect,
        ChatServerDisconnect,
        ChatJoinChannel,
        ChatLeaveChannel,
        Stacktrace,
             ]
