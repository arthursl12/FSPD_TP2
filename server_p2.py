#!/usr/bin/env python3

import argparse
from concurrent import futures  # for thread pool
import threading
import socket

import grpc

import part2_pb2
import part2_pb2_grpc

central_stored = {}

class ServicesCentralServer(part2_pb2_grpc.Part2ServicesServicer):
    def __init__(self, stop_event):
        self._stop_event = stop_event
    
    def register(self, request, context):
        """
        Receives the list of stored keys in a pair server and store them in
        central server. Note: already present keys will be overwritten.
        
        Returns (via RPC): 
            i: how many keys were processed
        """
        descr = request.descriptor
        i = 0
        
        # Adds or overwrites keys from the pair server into central server
        for ch in request.keys:
            central_stored[ch] = descr
            i += 1
        
        # Returns how many keys were processed (added or overwritten)
        return part2_pb2.IntReply(ret_integer=i)
        
    
    def map(self, request, context):
        """
        Similar to 'consult' of part 1, but now the response is which server
        to ask for desired key
        
        Returns:
            str: descriptor of pair server with requested key
            empty string: this key is not stored in any pair server registered
        """
        # Check if exists
        ch = request.integer
        search = central_stored.get(ch)
        if (search is None):
            # It is not in any registered server, return empty string (None)
            return part2_pb2.StrReply(s=None)
        else:
            # It is in a server, we return its descriptor
            return part2_pb2.StrReply(s=central_stored[ch])
    
    def terminate(self, request, context):
        """
        Terminates server execution
        
        Returns (via RPC): how many keys were stored in central server
        """
        self._stop_event.set()
        return part2_pb2.IntReply(ret_integer=len(central_stored))

def parseArguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="port to be used by server")
    parser.add_argument("control", help="control flag", 
                        nargs='?', default="")
    args = parser.parse_args()
    
    # Treating arguments
    port = int(args.port)
    
    control = args.control
    return port, control

def main():
    # Usage: python server_p2.py port [flag]
    port, control = parseArguments()
    
    # Create server
    stop_event = threading.Event()      # Termination event
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    part2_pb2_grpc.add_Part2ServicesServicer_to_server(ServicesCentralServer(stop_event),server)
    
    # Start server
    server.add_insecure_port(str(socket.INADDR_ANY)+':'+str(port))
    server.start()
    stop_event.wait()   # stop_event to be triggered in termination method
    server.stop(2)      # 2 seconds of grace
    
if __name__ == "__main__":
    main()
