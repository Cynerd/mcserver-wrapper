MINECRAFT-WRAPPER
=================
Python server wrapper for extracting informations about server status and list of
online players.

Requires:
-----------------
* Unix-like OS (preferred an only tested is Linux)
* Python3
* Dependencies for Minecraft server (Java)

Usage
-----------------
```
mcwrapper [arguments...] IDENTIFIER
  This script is executing Minecraft server and reads its output. From output is
  extracted server status and list of online players.

 arguments
   -h, --help
	   Prints this help text.
   -v, --verbose
	   Increase verbose level of output.
   -q, --quiet
	   Decrease verbose level of output.
    --config CONFIG_FILE
       Specify configuration file to be used.
    --configfile
       prints used configuration file and exits.

 IDENTIFIER
   Identifier for new server. This allows multiple servers running with this
   wrapper.  Identifier is word without spaces and preferably without special
   characters.
```

How it works
-----------------
Script is reading Minercraft server standard and error output. It's looking for
known lines that signals change of server output and players joining and leaving.
Minecraft server output is well designed for information parsing. Informations are
in exported to directory specified in configuration as `status`.

###Status file
This file is in status directory named as `status`.  If it exists, it specifies in
what status is server in the moment.
Status can be:
* Starting
* Running
* Stopping

If file not exists, then server is not running at all.

###Players file
This file in in status directory and is named as `players`. If server is running,
it contains online players. Player name per line.  If server isn't running, it
content don't have to be valid.

###Input pipe
This is unix pipe. This file is located in status directory and named as
`input_pipe`.  This pipe is input to Minercraft server standard input. If you have
write access rights (default 640), then you can send any command to Minecraft
server by writing to this pipe.

###Server.pid file
This file contains PID of Minecraft server process. This is used to detect if
server is running when status files exists. It has probably no usage for user, but
shouldn't be tempered with.

Configuration
-----------------
You can use `example.conf` as base configuration. Configuration file is in fact
Python3 script that is executed and its variables are used as configuration.
Script is searching for configuration in these files (in order of precedence):
 * mcwrapper.conf
 * mcwrapper.conf
 * ~/.mcwrapper.conf
 * ~/.config/mcwrapper.conf
 * /etc/mcwrapper.conf
Or you can use `--config` argument to specify any other file with valid content.
