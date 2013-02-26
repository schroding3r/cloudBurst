#!/usr/bin/python
import socket
import sys
import os

OWNER = 'schr0'
NETWORK = 'irc.freenode.net'
PORT = 6667
NICK = 'Schr0bot'
TRIGGER = '!'
ENCODING = 'utf-8' #Python3 modification, converts the strings to bytearrays before sending
INITCHAN = '#cyberia'
LOGFILE = 'cloudBurst.log'


log=open(LOGFILE,'a')
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect((NETWORK,PORT))
irc.send (('NICK {0}\r\n'.format(NICK)).encode(ENCODING))
irc.send (('USER {0} O O O\r\n'.format(NICK)).encode(ENCODING))
irc.send (('PRIVMSG NickServ :identify schr0bot\r\n').encode(ENCODING))
irc.send (('JOIN {0}\r\n'.format(INITCHAN)).encode(ENCODING))

def esend(message,chan):
        irc.send(('PRIVMSG '+chan+" :"+message+"\r\n").encode(ENCODING))
        
def command(sender,sendername,senderhost,sentto,arg):
        plugdir=sys.path[0]+'\\cloudBurstPlugins\\'
        plugins=os.listdir(plugdir)
        if arg == 'die':
                exit()
        if arg in plugins:
                execstage=plugdir+arg
               # log.write('Command Run:',end=' ') Weird bug needs looked into
                log.write('Command Run:')
                log.write(arg)
                exec(compile(open(execstage).read(),execstage,'exec'))
        else:
                esend("invalid command",sentto)

def think(line): #produce useful fields
        senderhostmask=line[0].split('!',1)
        sender=senderhostmask[0]        
        sender=sender[1:]
        fullsenderhost=''.join(senderhostmask[1:])
        _senderhost=fullsenderhost.split('@',1)
        senderhost=''.join(_senderhost[1:])
        try:
                sentto=line[2]
        except IndexError:
                sentto='null'
        try:
                message=line[3]
        except IndexError:
                message='null'
        message=message[1:]
        sendername=''.join(_senderhost[0])
        message=message.rstrip()
        if message.startswith(TRIGGER):
                message=message[:0]+message[1:] #removes trigger
                log.write('[*]command received: '+message+'')
                command(sender,sendername,senderhost,sentto,message)

while 1:
        try:
                line=((irc.recv(4096)).decode(ENCODING)) #recieve server messages 
                checkline=line.split(' ')
                if checkline[0]!='PING': #Call a parsing function
                        log.write(line)
                        procline=line.split(' ',3)
                        think(procline)
                if(checkline[0]=='PING'): #If server pings then pong
                        pongline=line.split(' ',1)
                        irc.send(('PONG '+pongline[1]).encode(ENCODING))
                if(checkline[1]=='JOIN'):
                        pass #might be used later
        except socket.error as msg:
                if line:
                        line.close()
                log.write('[X]Socket Error: '+msg)
        except IndexError as msg:
                log.write('[X]Short Message- Error: '+msg)
        except UnicodeDecodeError as msg:
                log.write('[X]Unicode Error: '+msg)
                
irc.close()

