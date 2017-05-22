Logs Submodule
==============

The Logs Submodule is the core parsing mechanism in Scon.
It defines classes for opening logfiles from zips, directories, or as a stream, and are intended to be used by higher level apis to adjust to the wanted log retrieval scenario, while keeping the base logic how logs are interpreted unified.

For the programmer, following submodules are of particular interest

Game
----

Contains all the Packets occuring in game.log; from an interpretation perspective, this holds data of joining games.

Combat
------

Contains all the Combat Packets, occuring during gameplay of any sort. From an interpretation perspective, this holds the juicy data about pew pew.

Chat
----

Contains chat packets. 

Session
-------

This is the module holding the session collector, trying to make it easy to access your logs and parse them.

