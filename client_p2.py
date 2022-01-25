#!/usr/bin/env python3

from __future__ import print_function  # used in stubs

import argparse
import sys

import grpc

import part1_pb2, part1_pb2_grpc, part2_pb2, part2_pb2_grpc


SEPARATOR = ','

def parseArguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("id_service", help="IP:port of central server")
    args = parser.parse_args()
    
    # Treating arguments
    ip_porta = str(args.id_service)
    return ip_porta

def executeCommands(stub):
    # Reading commands from standard input
    # (can be redirected from a file via "<" in terminal)
    for line in sys.stdin:
        line = ''.join(line.split())    # Remove all whitespaces from string

        # Execute commands
        if (line[0] == 'C'):
            # Consult operation 
            # First asks the central server, then, if found, asks returned 
            # regular server
            _, ch = line.split(SEPARATOR)
            ch = int(ch)
            response = stub.map(part2_pb2.IntRequest(integer=ch))
            
            # If key was found, connect to pair server returned and retrieve
            # requested string
            if (response.s != ""):
                # Prints descriptor of pair server (without ending in newline)
                print(f"{response.s}:",end='')

                # Connect to pair server
                channel = grpc.insecure_channel(response.s)
                sub_stub = part1_pb2_grpc.Part1ServicesStub(channel)
                
                # Do a Consult RPC and prints the result
                response = sub_stub.consult(part1_pb2.IntRequest(integer=ch))
                print(f"{response.s}")

                # Close connection to pair server
                channel.close()
            else:
                # Key not found, just print an newline
                print("")
            
        elif (line[0] == 'T'):
            # Terminate central server operation
            # Prints the return value (integer), i.e., 0 and exits
            response = stub.terminate(part2_pb2.EmptyRequest())
            print(f"{response.ret_integer}")
            exit()
        else:
            # Unknown command, just skip it
            pass
    # End of commands, client may end now
            
def main():
    # Usage: ./client_p2.py <IP:port>
    #   Must be given execution permission first (via 'chmod +x client_p2.py')
    ip_porta = parseArguments()
    
    # Connect to central server
    channel = grpc.insecure_channel(ip_porta)
    stub = part2_pb2_grpc.Part2ServicesStub(channel)
    
    # Execute commands
    executeCommands(stub)
    
    # Close connection to central server
    channel.close()
        

if __name__ == "__main__":
    main()
