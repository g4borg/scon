

# LogStream
"""
    A LogStream is supposed to:
     - parse data feeded into it.
     - yield new objects
     - remember errors
    
    LogStream.Initialize:
     - initialize the logstream in some way.
    
    LogStream.Next:
     - once initialized, read your stream until you can yield a new class
     the next function reads the read-stream ahead.
     empty lines are omitted
     it tries to match the data into a new class and yields it
     if it runs into trouble, it just outputs the line for now.
    
    InitializeString:
     - init with a data blob
     - nice for trying it on files
    
    @TODO: look at how file streams in python are implemented and find a good generic solution
    combine it with the lookup for "watching files being changed", to create a program which listens to the logs live
    @see: monitor.py
    @see: watchdog https://pypi.python.org/pypi/watchdog
"""