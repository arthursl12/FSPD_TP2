#!/usr/bin/env python

import argparse
import logging
import sys
from concurrent import futures  # for thread pool
import threading
from google.protobuf import descriptor
import socket

import grpc
import part1_pb2, part1_pb2_grpc, part2_pb2, part2_pb2_grpc

log = logging.getLogger(__name__)
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
        log.debug(f"[GRPC] Insert, ch={request.ch}, s={request.s}")
        # Check if exists
        search = stored.get(request.ch)
        if (search is None):
            # It does not exist, we can add it and return 0
            log.debug(f"[GRPC] It does not exist")
            stored[request.ch] = request.s
            return part1_pb2.IntReply(ret_integer=0)
        else:
            # It exists already, we just return -1
            log.debug(f"[GRPC] It exists")
            return part1_pb2.IntReply(ret_integer=-1)
    
    def consult(self, request, context):
        """
        Consult dictionary entry with key 'ch'
        
        Returns (via RPC):
            s: the string with key 'ch'. If it doesn't exist, returns None
        """
        log.debug(f"[GRPC] Consult, ch={request.integer}")
        # Check if exists
        ch = request.integer
        search = stored.get(ch)
        if (search is None):
            # It does not exist, return null (None) string
            log.debug(f"[GRPC] It does not exist, returning null")
            return part1_pb2.StrReply(s=None)
        else:
            # It exists already, we just return it and its key
            log.debug(f"[GRPC] It exists, returning it")
            return part1_pb2.StrReply(s=stored[ch])
    
    def activate(self, request, context):
        """
        Part1: Simply returns 0 (via RPC)
        
        Part2: Connect pair server (itself) to central server located by 
        description string passed as parameter and send a RPC to register itself
        there. Returns the integer returned by the central server. 
        """
        log.debug(f"Activate is: {self.activate_part_2}")
        if (self.activate_part_2):
            print(f"[GRPC] Activate (part2), s={request.s}")
            
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
            # Just return 0
            print(f"[GRPC] Activate (part1), s={request.s}")
            return part1_pb2.IntReply(ret_integer=0)
    
    def terminate(self, request, context):
        """
        Terminates server execution
        
        Returns (via RPC): 0 on sucessfull termination
        """
        print(f"[GRPC] Terminate")
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
    log.debug(f"We'll connect at {port}")
    
    control = args.control
    if (control): log.debug(f"Control flag is: {control}")
    return port, control

def main():
    # Usage: ./server_p1.py port [flag]
    port, control = parseArguments()
    descriptor = str(socket.INADDR_ANY)+':'+str(port)
    
    # Activate part2 behaviour, if needed
    activate_part_2 = False
    if (control is not None):
        activate_part_2 = True
    log.debug(f"Activate is: {activate_part_2}")
    
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
    
    # Definir o nível de logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()
