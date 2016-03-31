MCSERVER-WRAPPER
================
Minecraft server wrapper written in Python3 that extracts server status and list
of online players.

Requires:
-----------------
* Unix-like OS (preferred an only tested is Linux)
* Python3 (minimum version 3.3)
* Dependencies for Minecraft server (Java)

For releasing are required also Pandoc and pypandoc to convert this file.

Installation
------------
Installation is done using `pip`. Execute this command to install:
```
sudo pip install mcserver-wrapper
```
Expecting that Python3 is your default Python version, otherwise use `pip3`.

MCWRAPPER
---------
### Usage
```
mcwrapper [-h] [--verbose] [--quiet] [--status-file] [--players-file]
          ...

This script is executing Minecraft server and reads its output. From output is
extracted server status and list of online players. And standard input can be
accessed by fifo file.

positional arguments:
  command             Command to be executed to start Minecraft server.

optional arguments:
  -h, --help          show this help message and exit
  --verbose, -v       Increase verbose level of output
  --quiet, -q         Decrease verbose level of output
  --status-file, -s   Outputs server status to file "status"
  --players-file, -p  Outputs list of online players to file "players"
```

### How it works
Script is reading Minercraft server standard and error output. It's looking for
known lines that signals change of server status and players joining and leaving.
Minecraft server output is well designed for information parsing. Informations are
exported to directory working directory or websocket server.

#### Input pipe
This is unix pipe. This file is located in working directory and named as
`input_pipe`.  This pipe is input to Minercraft server standard input. If you have
write access rights (default 640), then you can send any command to Minecraft
server by writing to this pipe.

#### Server.pid file
This file contains PID of Minecraft server process. This is used to detect if
server is running when status files exists. It has probably no usage for user, but
shouldn't be tempered with.

#### Status file
This file is in working directory and is named as `status`. If it exists, it
specifies in what status is server in the moment.
Status can be:

* Starting
* Running
* Stopping

If file not exists, then server is not running at all.

#### Players file
This file in in status directory and is named as `players`. If server is running,
it contains online players. Player name per line.  If server isn't running, it
content don't have to be valid.

MCWRAPPER-TERMINAL
------------------
This application is going to be used for interactive terminal access to minecraft
server console. It should use latest minecraft server log as input and output will
be pushed to input pipe of mcwrapper.  This app is currently in development.
