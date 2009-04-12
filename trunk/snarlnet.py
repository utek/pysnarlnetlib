#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
pySnarlNetLib
author: Łukasz Bołdys
licence: MIT 

Copyright (c) 2009 Łukasz Bołdys

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.


"""
import sys
import socket

__version__ = (0, 1, 1)
__author__ = "Łukasz Bołdys"


class SnarlNet(object):    
    lastAppName = ""
    lastClassName = ""
    addedClasses = []
    lastTimeout = 10
    ip = "127.0.0.1" #if no ip provided than use localhost
    port = 9887 #if no port provided than use default snarl net port
    
    def __init__(self, *args, **argv):
        """
        Create object of class SnarlNet
        IP and port can be passed as 'ip' and 'port' parameters
        Ie. snarl = SnarlNet(ip="192.168.1.4", port=9887)
        When no parameters are passed than ip='127.0.0.1' and port=9887 are used
        
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if argv.has_key("ip"):
            self.ip = argv["ip"]        
        if argv.has_key("port"):
            self.port = argv["port"]
    
    def __send(self, sendStr):
        self.sock.connect((self.ip, self.port))
        self.sock.send(sendStr)
        self.sock.close()
    
    def register(self, appName):
        """
        Register application by appName
        
        """
        sendStr = "type=SNP#?version=1.0#?action=register#?app=%s\r\n" % (appName,)
        self.__send(sendStr)
        self.lastAppName = appName;
        
    def unregister(self, appName = ""):
        """
        Unregister application by appName. If appName is empty then tries to
        unregister application by self.lastAppName (last registred application).
        If self.lastAppName is empty than do nothing
        
        """
        if appName == "":
            if lastAppName == "":
                sys.stderr.write("No application to unregister")
                return
            appName = lastAppName
        sendStr = "type=SNP#?version=1.0#?action=unregister#?app=%s\r\n" % (appName,)
        self.__send(sendStr)
        self.lastAppName = ""        
    
    def notify(self, title, text, **argv):
        """
        Send message with given title and text.
        If no appName or appClass is provided than uses
        self.lastAppName and/or self.lastClassName
        
        """
        appName = self.lastAppName
        className = self.lastClassName
        timeout = self.lastTimeout
        if argv.has_key("timeout"):
            timeout = timeout
        if argv.has_key("appName") and argv["appName"] != "":
            appName = argv["appName"]
        if argv.has_key("className") and argv["className"] != "":
            className = argv["className"]
        if appName == "":
            appName = "pySnarlNetLib"
        if className == "":
            className = "pySnarlNetLibClass"
        sendStr = "type=SNP#?version=1.0#?action=notification#?app=%s#?class=%s#?title=%s#?text=%s#?timeout=%d\r\n" % (appName,className,title,text,timeout)
        self.__send(sendStr)
        self.lastAppName = appName
        self.lastClassName = className
        self.lastTimeout = timeout
        
        pass
    
    def addclass(self, className, classTitle="", **argv):
        """
        Add class with provided name (className).
        If no classTitle is provided than sets classTitle to className
        If no appName is provided than use self.lastAppName.
        If self.lastAppName is empty than do nothing
        
        """
        className = str(className)
        if className in self.addedClasses:
            sys.stderr.write("Class already added")
            return
        if className == "":
            sys.stderr.write("className can not be empty")
            return
        appName = self.lastAppName        
        if classTitle == "":
            classTitle = className
        if argv.has_key["appName"]:
            appName = argv["appName"]
        if appName == "":
            sys.stderr.write("No application to add class to")
            return
        sendStr = "type=SNP#?version=1.0#?action=add_class#?app=%s#?class=%s#?title=%s\r\n" % (appName,className,classTitle)
        self.__send(sendStr)
        self.lastAppName = appName
        self.lastClassName = className
        self.addedClasses.append(className)
        
if __name__ == '__main__':
    from optparse import OptionParser
    
    parser = OptionParser(usage="%prog -a ACTION [options] args", version="%prog " + ".".join([str(x) for x in __version__]))
    parser.add_option("-i", "--ipaddr", dest="host",
                      help="IP address of the machine with snarl installed (default: %default)",
                      type="string", default="127.0.0.1")
    parser.add_option("-p", "--port", dest="port",
                      help="Port on with Snarl is listening (default: %default)",
                      type="int", default=9887)
    parser.add_option("-n", "--appname", dest="appName", help="Application name",
                      type="string")
    parser.add_option("-c", "--classname", dest="className", help="Class name",
                      type="string")
    parser.add_option("-a", "--action", dest="action", choices=["register","unregister","addclass","notify"],
                      help="Action to take (register, unregister, addclass, notify)", type="choice")
    parser.add_option("-t", "--timeout", dest="timeout", type="int",
                      help="How long snarl should display message", default=10)
    
    (options, args) = parser.parse_args()
    snarl = SnarlNet(ip=options.host, port=options.port)
    
    if not options.action:
        parser.print_usage()
    if options.action == "register":
        if options.appName != None:
            appName = options.appName
        elif len(args) > 0:
            appName = args[0]
        else:
            parser.error("You need to provide application name")
        snarl.register(appName)
    elif options.action == "unregister":
        if options.appName != None:
            appName = options.appName
        elif len(args) > 0:
            appName = args[0]
        else:
            parser.error("You need to provide application name")
        snarl.unregister(appName)
    elif options.action == "addclass":
        if options.appName != None and options.className != None:
            appName = options.appName
            className = options.className            
        elif options.appName != None and options.className == None:
            appName = options.appName
            if len(args) == 1:
                className = args[0]
            else:
                parser.error("You need to provide class name")
        elif options.appName == None and options.className != None:
            className = options.className
            if len(args) == 1:
                appName = args[0]
            else:
                parser.error("You need to provide application name")
        else:
            if len(args) > 1:
                appName = args[0]
                className = args[1]
                parser.error("You need to provide application name and class name")
        snarl.addclass(className, classTitle=options.classTitle, appName=appName)
    elif options.action == "notify":
        appName = ""
        className = ""
        if options.appName != None:
            appName = options.appName
        if options.className != None:
            className = options.className
        if len(args) > 0:
            title = args[0]
            text = " ".join(args[1:])
        else:
            parser.error("You need to provide at least a title")
        snarl.notify(title, text, appName=appName, className=className)
        