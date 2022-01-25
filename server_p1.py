#!/usr/bin/env python3

import argparse
from concurrent import futures  # for thread pool
import threading
import socket

import grpc
import part1_pb2, part1_pb2_grpc, part2_pb2, part2_pb2_grpc

stored = {}

class ServicesPairServer(part1_pb2_grpc.Part1ServicesServicer):
    def __init__(self, stop_event, port, activate_part_2):
        self._stop_event = stop_event
        self.descriptor = socket.getfqdn()+':'+str(port)
        self.activate_part_2 = activate_part_2
        
    def insert(self, request, context):
        """
        Insert string 's' into dictionary with key 'ch'
        
        Returns (via RPC):
            0 if it was added sucessully
            -1 if an entry with this key already existed, nothing was done
        """
        # Check if exists
        search = stored.get(request.ch)
        if (search is None):
            # It does not exist, we can add it and return 0
            stored[request.ch] = request.s
            return part1_pb2.IntReply(ret_integer=0)
        else:
            # It exists already, we just return -1
            return part1_pb2.IntReply(ret_integer=-1)
    
    def consult(self, request, context):
        """
        Consult dictionary entry with key 'ch'
        
        Returns (via RPC):
            s: the string with key 'ch'. If it doesn't exist, returns None
        """
        # Check if exists
        ch = request.integer
        search = stored.get(ch)
        if (search is None):
            # It does not exist, return null (None) string
            return part1_pb2.StrReply(s=None)
        else:
            # It exists already, we just return it and its key
            return part1_pb2.StrReply(s=stored[ch])
    
    def activate(self, request, context):
        """
        Part1: Simply returns 0 (via RPC)
        
        Part2: Connect pair server (itself) to central server located by 
        description string passed as parameter and send a RPC to register itself
        there. Returns the integer returned by the central server. 
        """
        if (self.activate_part_2):
            # Connect to central server
            channel = grpc.insecure_channel(request.s)
            stub = part2_pb2_grpc.Part2ServicesStub(channel)
            
            # Register itself there
            response = stub.register(part2_pb2.RegisterRequest(descriptor=self.descriptor, keys=stored))
            
            # Close connection to central server
            channel.close()
            
            # Send response back to client
            return part1_pb2.IntReply(ret_integer=response.ret_integer)
        else:
            # Part1 behaviour: just return 0
            return part1_pb2.IntReply(ret_integer=0)
    
    def terminate(self, request, context):
        """
        Terminates server execution
        
        Returns (via RPC): 0 on sucessfull termination
        """
        self._stop_event.set()
        return part1_pb2.IntReply(ret_integer=0)

def parseArguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="port to be used by server")
    parser.add_argument("control", help="control flag", 
                        nargs='?', default=None)
    args = parser.parse_args()
    
    # Treating arguments
    port = int(args.port)
    
    control = args.control
    return port, control

def main():
    # Usage: ./server_p1.py port [flag]
    port, control = parseArguments()
    descriptor = str(socket.INADDR_ANY)+':'+str(port)
    
    # Activate part2 behaviour, if needed
    activate_part_2 = False
    if (control is not None):
        activate_part_2 = True
    
    # Create server
    stop_event = threading.Event()      # Termination event
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    part1_pb2_grpc.add_Part1ServicesServicer_to_server(
        ServicesPairServer(stop_event, port, activate_part_2),server)
    
    # Start server
    server.add_insecure_port(descriptor)
    server.start()
    stop_event.wait()   # stop_event to be triggered in termination method
    server.stop(2)      # 2 seconds of grace
    
if __name__ == "__main__":
    main()
