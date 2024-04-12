This file contains information on how to setup, install, run, and troubleshoot problems for project Bubble.

There are 3 steps that are required to be done to run the program successfully

1. installing packages and modules
2. establishing connections
3. running the bash script

Directory Structure:

Root: ~/Bubbles/
The Bubbles directory is structured with documentation and .json files loose in the root directory of Bubbles, alongside two subdirectories titled 'node_modules' and 'src'. 
There is also 'server.js' file which is called by the bash script 'startProgram.sh'. For the purposes of this prototype the 'startProgram.sh' functions as the executable/shortcut for Bubbles. 
As the subdirectory names imply, 'node_modules' contains all of the node modules used by Bubbles, while 'src' contains the source code responsible for its operation.

~/Bubbles/src/
The src subdirectory consists of five subdirectories, detailed as follows:

~/Bubbles/src/cssFiles
Contains the CSS files used by Bubbles.
~/Bubbles/src/htmlCode
Contains the HTML pages used by Bubbles.
~/Bubbles/src/img
Contains the image files used by Bubbles.
~/Bubbles/src/mySQL
Contains the database file used to establish the necessary tables for Bubbles.
~/Bubbles/src/python
Contains the python code which connects the database to the server and frontend of Bubbles. The 'databaseConnector.py' connects the database to the server and makes calls using a class defined in 'databaseclass.py'.
There is also a 'hash.py' file which defines the hashing functionality used by the database for the user passwords.

Bubbles Compilation and Execution:

It is highly recommended to use GitHub codespace to open/run files as well as installing packages.

creating a codespace:
	1. open https://github.com/Saad3123/Bubble 
	2. click "code" (green button)
	3. click "create codespace" -> open it

1. Installing Packages

	a. run pip install -r requirements.txt
	b. check whether node.js is installed by 
		> node -v
	if not, install it 
		> npm install node
	

2. Establishing connections
	There are 3 connections you need to make sure are being connected when the code is running.
	3306 for connecting dolphin
	3002 for node
	5000 for backend operations

	To successfully connect to dolphin you need to have configured ssh keys to csci
	a. to check whether they exist
		> ls ~/.ssh
	this should contain "id_rsa" (Contains the private key of the pair) and "id_rsa.pub" (Contains the public key of the pair)

	b. if not you can create by following steps in "Configure SSH keys" from http://csci.viu.ca/~wesselsd/guides/Tutorial-sshClient.html

3. Once everything is setup successfully, run 
	  > ./startProgram <CSCI lab username>
	Then enter your SSH password when prompted.
	Open port "3002" in a web browswer
	
At this point you should be looking at the Bubbles login page, where you can sign-in or sign-up to begin chatting.

