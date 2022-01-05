#!/usr/bin/env python

from __future__ import print_function  # used in stubs

import argparse
import logging
import os  # for getpid
import sys

import grpc

import part1_pb2
import part1_pb2_grpc

log = logging.getLogger(__name__)

SEPARATOR = ','

def parseArguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("id_service", help="IP:port of server")
    args = parser.parse_args()
    
    # Treating arguments
    ip_porta = str(args.id_service)
    log.debug(f"We'll connect to server at {ip_porta}")
    return ip_porta

def executeCommands(stub):
    # Reading commands from standard input
    # (can be redirected from a file via "<" in terminal)
    for line in sys.stdin:
        line = ''.join(line.split())    # Remove all whitespaces from string
        # log.debug(f"Read: {line};")
        
        # Execute commands
        if (line[0] == 'I'):
            # Insert operation
            # Prints the return value (integer)
            _, ch, dest = line.split(SEPARATOR)
            ch = int(ch)
            response = stub.insert(part1_pb2.InsertRequest(ch=ch, s=dest))
            print(f"{response.ret_integer}")
        elif (line[0] == 'C'):
            # Consult operation
            # Prints the consulted string returned (can be None)
            _, ch = line.split(SEPARATOR)
            ch = int(ch)
            response = stub.consult(part1_pb2.IntRequest(integer=ch))
            print(f"{response.s}")
        elif (line[0] == 'A'):
            # Activate operation
            # Prints the return value (integer), for now, 0
            _, dest = line.split(SEPARATOR)
            response = stub.activate(part1_pb2.StrRequest(s=dest))
            print(f"{response.ret_integer}")
        elif (line[0] == 'T'):
            # Terminate server operation
            # Prints the return value (integer), i.e., 0 and exits
            response = stub.terminate(part1_pb2.EmptyRequest())
            print(f"{response.ret_integer}")
            exit()
        else:
            # Unknown command, just skip it
            pass
    # End of commands, client may end now
            
def main():
    # Usage: python client_p1.py <IP:port>
    ip_porta = parseArguments()
    
    # Connect to server
    channel = grpc.insecure_channel(ip_porta)
    stub = part1_pb2_grpc.Part1ServicesStub(channel)
    
    # Execute commands
    executeCommands(stub)
    
    # Close connection to server
    channel.close()
        

if __name__ == "__main__":
    # Define logging level 
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()
