#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Monitor a StarConflict Log Directory.
"""
import sys, os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class SconEventHandler(LoggingEventHandler):
    def __init__(self, monitor, *args, **kwargs):
        self.monitor = monitor
        return super(SconEventHandler, self).__init__(*args, **kwargs)
    
    def on_moved(self, event):
        super(SconEventHandler, self).on_moved(event)
        if not event.is_directory:
            self.monitor.close(event.src_path)
        self.monitor.notify_event('moved', {'src': event.src_path, 
                                            'is_dir': event.is_directory, 
                                            'dest': event.dest_path})

    def on_created(self, event):
        super(SconEventHandler, self).on_created(event)
        if not event.is_directory:
            self.monitor.open(event.src_path)
        self.monitor.notify_event('created', {'src': event.src_path, 
                                              'is_dir': event.is_directory})

    def on_deleted(self, event):
        super(SconEventHandler, self).on_deleted(event)
        if not event.is_directory:
            self.monitor.close(event.src_path)
        self.monitor.notify_event('deleted', {'src': event.src_path, 
                                              'is_dir': event.is_directory})

    def on_modified(self, event):
        super(SconEventHandler, self).on_modified(event)
        self.monitor.notify_event('modified', {'src': event.src_path, 
                                              'is_dir': event.is_directory})
        
        

class SconMonitor(object):
        
    def notify(self, filename, lines):
        # notify somebody, filename has a few lines.
        # this is basicly the function you want to overwrite.
        # @see: self.run for how to integrate monitor into your main loop.
        if self.notifier is not None:
            self.notifier.notify(filename, lines)
    
    def notify_event(self, event_type, data):
        if self.notifier is not None:
            self.notifier.notify_event(event_type, data)
    
    def __init__(self, path=None, notifier=None):
        # if you initialize path directly, you lose success boolean.
        # albeit atm. this is always true.
        if path is not None:
            self.initialize(path)
        self.notifier = notifier
    
    def initialize(self, path):
        # initialize the monitor with a path to observe.
        self.files = {}
        self.event_handler = SconEventHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, 
                               path, 
                               recursive=True)
        return True
    
    def open(self, filename=None):
        # open a logfile and add it to the read-list...
        f = open(filename, 'r')
        new_file = { 'file': f,
                     'cursor': f.tell() }
        self.files[filename] = new_file
        return new_file
    
    def close(self, filename):
        # close a single file by key, does not do anything if not found.
        if filename in self.files.keys():
            close_file = self.files.pop(filename)
            close_file['file'].close()
            del close_file
    
    def close_all(self):
        """ closes all open files in the monitor """
        for key in self.files.keys():
            self.close(key)
    
    def read_line(self, afile):
        # read a single line in a file.
        f = afile.get('file', None)
        if f is None:
            return
        afile['cursor'] = f.tell()
        line = f.readline()
        if not line:
            f.seek(afile['cursor'])
            return None
        else:
            return line
    
    def do(self):
        ''' Monitor main task handler, call this in your mainloop in ~1 sec intervals '''
        # read all file changes.
        for key, value in self.files.items():
            lines = []
            data = self.read_line(value)
            while data is not None:
                lines.append(data)
                data = self.read_line(value)
            if lines:
                self.notify(key, lines)
            # 
    
    def initialize_loop(self):
        ''' initializes the main loop for the monitor '''
        self.observer.start()
    
    def break_loop(self):
        ''' call this if you want to break the monitors tasks '''
        self.observer.stop()
    
    def end_loop(self):
        ''' always call this before exiting your main loop '''
        self.close_all()
        self.observer.join()
        
    def run(self):
        ''' Basic Standalone Main Loop implementation, do not call this in your app. '''
        # if you want to run this on its own.
        # everytime any logfile is updated, print it.
        self.initialize_loop()
        try:
            while True:
                self.do()
                time.sleep(1)
        except KeyboardInterrupt:
            self.break_loop()
        self.end_loop()

if __name__ == '__main__':
    monitor = SconMonitor()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',
                                     'logs'
                                     )
    if monitor.initialize(path) is True:
        monitor.run()
    