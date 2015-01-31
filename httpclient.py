#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Tarek El Bohtimy
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        if url[0:4]!="http":
            if url.count(":")==1:
                port=url.split(":")
                port=port[1].split("/")[0]
                return port
            else:
                return 80
        else:
            if url.count(":")==2:
                port=url.split("/")
                port=port[2].split(":")
                return int(port[1])
            else:   
                return 80      
    def get_host(self,url):
         if url[0:4]!="http":
             if url.count(":")==1:
                 host=url.split(":")
                 host=host[0].strip("/")
                 return host
             else:
                 host=url.split("/")
                 host=host[0]
                 return host        
         else:  
             if url.count(":")==2:
                 host=url.split(":")
                 host=host[1].strip("/")
                 return host
             else:
                 host=url.split("/")
                 host=host[2]
                 return host
    def get_path(self,url):
        if url[0:4]!="http":
            start=1  
        else:
            start=3
        newpath=""
        path=url.split("/")
        for i in range(start,len(path)):
            newpath+="/"+path[i]
        if newpath=="":
            newpath="/"
        return newpath
    def connect(self, host, port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,port))
        return s

    def get_code(self, data):
        code=data.split("\r\n")
        code=data.split(" ")[1]
        return int(code)

    def get_headers(self,data):
        data=data.split("\r\n\r\n")
        return data[0]

    def get_body(self, data):
        data=data.split("\r\n\r\n")
        return data[1]
    
    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code=500
        body=""
        path=self.get_path(url)
        host=self.get_host(url)
        port=self.get_host_port(url)
        s=self.connect(host,port)

        httpGet="GET "+path+" HTTP/1.1\r\n"
        httpGet+="Host: "+host+"\r\n"
        httpGet+="Accept: */*\r\n\r\n"
        s.send(httpGet)
        data=self.recvall(s)
        s.close()
 
        code=self.get_code(data)
        body=self.get_body(data)
 
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        path=self.get_path(url)
        host=self.get_host(url)
        port= self.get_host_port(url)
      
        s=self.connect(host,port)
        httpPost="POST "+path+" HTTP/1.1\r\n"
        httpPost+="Host: "+host+"\r\n"
        httpPost+="Accept: */*\r\n"
        httpPost+="Content-Type: application/x-www-form-urlencoded\r\n"
        if args != None:
            argsEncode=urllib.urlencode(args)
            length=str(len(argsEncode))
            httpPost+="Content-Length: "+length+"\r\n\r\n"
            httpPost+=argsEncode
        else:
            httpPost+="Content-Length: 0\r\n\r\n"
        s.send(httpPost)
        
        data=self.recvall(s)
    
        s.close()
        code=self.get_code(data)
        body=self.get_body(data)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )
      
