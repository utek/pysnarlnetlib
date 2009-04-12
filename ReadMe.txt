pySnarlNetLib
author: Łukasz Bołdys
licence: MIT


Library written in pure python that uses socket to send commands to Snarl.

Current commands:

    * register
    * unregister
    * addclass
    * notification 


To use it in your code:

    >>import snarlnet    
    >>snarl = snarlnet.SnarlNet(ip="127.0.0.1", port=9887)
    >>snarl.notify("Some title", "Some text")

snarlnet.py can be run from command line.


Usage:

    snarlnet.py -a ACTION [options] args
    
    Options:
      -h, --help            show this help message and exit
      -i HOST, --ipaddr=HOST
                            IP address of the machine with snarl installed
                            (default: 127.0.0.1)
      -p PORT, --port=PORT  Port on with Snarl is listening (default: 9887)
      -n APPNAME, --appname=APPNAME
                            Application name
      -c CLASSNAME, --classname=CLASSNAME
                            Class name
      -a ACTION, --action=ACTION
                            Action to take (register, unregister, addclass,
                            notify)
      -t TIMEOUT, --timeout=TIMEOUT
                            How long snarl should display message

example:
    snarlpy.py -a notify Title "Some message" -t 20