Logs Submodule
==============

The Logs Submodule is the core parsing mechanism in Scon.
It defines classes for opening logfiles from zips, directories, or as a stream, and are intended to be used by higher level apis to adjust to the wanted log retrieval scenario, while keeping the base logic how logs are interpreted unified.

The Parsing Mechanism
---------------------
In this example, parsing complete files:

* The ``LogSessionCollector`` is a helper class to build sessions from a directory containing many log-directories, i call sessions.
* The ``Session`` represents a container which hold logfiles from the same directory.
	- it can open zipped logs aswell as directories
	- it has a parse_files method which initiates first pass parsing for the given filenames in the package.
	- only 'game.log', 'combat.log' and 'chat.log' are supported for now as session.game_log, session.combat_log and session.chat_log.
	- you are able to parse just a subset of those files, e.g. first only game log, later combat or chat.
* The ``Logfile`` class directly has 'lines' property holding all the 'lines from the log'. Each kind of logfile has its own subclass in logfiles.
* this ``lines`` list is converted from a string list to dictionaries, containing 'log', 'logtype', and split timestamp data in the first parsing.
  As you might know, this is the same for all logs in SC
* these dicts are scanned by the class factories and replaced with class based representations of the log packet, coming from their submodule.
	- the dict is moved into the dict .values of the created class.
	- this is the first pass that happens if you call parse_files.
* usually at this point, one would discard all dicts, as they represent unknown or unimportant data, what you have left is a list of classes. this is optional.
	
from here, all lines contain some instance of a class, already telling us, which kind of log this is, by its class itself,
however to update the rest of the log information, one has to at least call "unpack" once on the instance.
having this finetuned in multiple steps however allows us to gain speed by ignoring unwanted information (as combat logs e.g. tend to be large)
all other functionality is planend to be in the high level api .game
	
e.g.::

	for line in game_log.lines:
	  if isinstance(line, Log):
	    if line.unpack():
	      print(line.values.keys())

	
| *unpack can be called several times, as it only unpacks once.*

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

