Note on windows:
	- if you virtualenv python3, make sure to copy following data over to your newly created virtualenv:
		* copy Python3.dll in main python directory -> virtualenv/Scripts
			- needed for Qt5, so gui based things. not needed if you use the library only.
			- a dll called Python3x.dll should already exist there.
		* tcl directories need to be copied over for some libraries using it 
			- (this project currently does not need that)
