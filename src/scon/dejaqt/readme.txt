I am always happy if a project spawns another project.

In this case DejaQt, a little django-qt bridge for yet another attempt to
ease up programming for myself - and possibly for others.

Basicly, the theory is the following:
 - I create a Django App, that might run on a server.
 - But I actually want to make a standalone app too, which is executable, too
   Maybe even deploy an EXE with py2exe, and so on.
 - The standalone might have a lot more local functionality,
   But also shared codebase, with database, forms, etc.
 - I do not want shared code to be executed in a local webserver and create
   a network client to it. This is just too much abstraction, for a simple task.
   Not to speak about security...
   I also do not want to create two different codebases to do the same stuff.
 - Instead, I want a QWebView, using WebKit, which can call views and urls internally
   without actually starting up a django server instance, but still use django
 
 DejaQt wants actually this.
 
 Roadmap:
  - PyQt4 base implementation
  - GET and POST requests, and file transfers.
  - Basic setup layout:
    * define directories for file transfers
    * save client