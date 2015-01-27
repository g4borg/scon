#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Monitor StarConflict Logs
    
"""
import sys, os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class SconMonitor(object):
    
    def initialize(self, path):
        # initialize the monitor.
        self.event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, 
                               path, 
                               recursive=True)
        
    
        
        # return true if successful
        return True
    
    def open(self, filename=None):
        # open the logs.
        pass
    
    def check_running(self):
        # maybe check if the exe is running? 
        return True
    
    def run(self):
        # everytime the logfile is updated, print it.
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
    
    def output(self, line):
        print line

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
    