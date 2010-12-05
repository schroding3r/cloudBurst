#!/usr/bin/python
import socket
import sys
import os

OWNER = 'Schro'
NETWORK = '67.58.179.252'
PORT = 56667
NICK = 'CloudBurst'
TRIGGER = '!'
ENCODING = 'utf-8' #Python3 modification, converts the strings to bytearrays before sending
INITCHAN = '#cyberia'

plugdir=sys.path[0]+'\\cloudBurstPlugins\\'
plugins=os.listdir(plugdir)

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect((NETWORK,PORT))
irc.send (('NICK {0}\r\n'.format(NICK)).encode(ENCODING))
irc.send (('USER {0} O O O\r\n'.format(NICK)).encode(ENCODING))
irc.send (('PRIVMSG NickServ :identify schr0bot\r\n').encode(ENCODING))
def command(arg):
        if arg=='!join':
                print ('[*]attempting to join')
                irc.send(('JOIN '+INITCHAN+'\r\n').encode(ENCODING))
        if arg=='!die':
                print ('[*]shutting down...')
                exit()
        if arg=='!availPlug':
                print ('[*]Listing Plugins')
                print ('[*]Loaded Plugins:',end=' ')
                print (plugins)

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
                print ('[*]command received: '+message+'')
                command(message)

while 1:
        try:
                line=((irc.recv(4096)).decode(ENCODING)) #recieve server messages
                print (line) 
                checkline=line.split(' ')
                if checkline[0]!='PING': #Call a parsing function
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
                print ('[X]Socket Error: '+msg)
        except IndexError as msg:
                print ('[X]Short Message- Error: '+msg)
        except UnicodeDecodeError as msg:
                print ('[X]Unicode Error: '+msg)
                
irc.close()

