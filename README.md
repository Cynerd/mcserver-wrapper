MINECRAFT-WRAPPER
=================

Python server wrapper for extracting informations about server status and list of online players.

Requires:
-----------------
* Unix-like OS (preferred an only tested is Linux)
* Python3
* Dependencies for Minecraft server (Java)

Usage
-----------------
```
mcwrapper ACTION {IDENTIFIER} [args...]
  This script is executing Minecraft server and reads its output. From output is extracted server
  status and list of online players.

 ACTION
   start  Starts server specified with IDENTIFIER. As arguments takes command line for starting
          Minecraft server.
   stop   Sends stop command to Minecraf server specified with IDENTIFIER.
   say    Sends arguments to server chat as server message. Server is specified using IDENTIFIER.

 IDENTIFIER
   Identifier can be any word without spaces and preferably without special characters.
   It is used for identifying server instances, so that multiple servers can run with
   this wrapper on single system.
```

How it works
-----------------
Script is reading Minercraft server standard and error output. It's looking for
known lines that signals change of server output and players joining and leaving.
Minecraft server output is well designed for information parsing. Informations are
in default exported to folder /dev/shm/mcwrapper_IDENTIFIER where IDENTIFIER is
specified as argument to script. From now on will be replaced with *.

###Status file
This file is in default configuration in path `/dev/shm/mcwrapper_*/status`.
If it exists, it contains in what status is server in the moment.
Status can be:
* Starting
* Running
* Stopping

If file not exists, then server is not running at all.

###Players file
This file in in default configuration in path `/dev/shm/mcwrapper_*/players` If
server is running, it constains online players. Player name per line.  If server
isn't runnint, it content don't have to be valid.

##Input pipe
This is unit pipe. In default configuration is in path
`/dev/shm/mcwrapper_*/input_pipe`.  This pipe is input to Minercraft server
standard input. If you have write access rights (default 640), then you can send
any command to Minecraft server by writing to this pipe.
