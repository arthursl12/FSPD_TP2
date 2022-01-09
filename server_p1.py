#!/usr/bin/env python

import argparse
import logging
import sys
from concurrent import futures  # for thread pool
import threading

import grpc

import part1_pb2
import part1_pb2_grpc

log = logging.getLogger(__name__)
stored = {}
class ServicesPart1(part1_pb2_grpc.Part1ServicesServicer):
    def __init__(self, stop_event):
        self._stop_event = stop_event
        
    def insert(self, request, context):
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
        print(f"[GRPC] Activate, s={request.s}")
        return part1_pb2.IntReply(ret_integer=0)
    
    def terminate(self, request, context):
        print(f"[GRPC] Terminate")
        self._stop_event.set()
        return part1_pb2.IntReply(ret_integer=0)

def parseArguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="port to be used by server")
    parser.add_argument("control", help="control flag", 
                        nargs='?', default="")
    args = parser.parse_args()
    
    # Treating arguments
    port = int(args.port)
    log.debug(f"We'll connect at {port}")
    
    control = args.control
    if (control): log.debug(f"Control flag is: {control}")
    return port, control

def main():
    # Usage: python server_p1.py port [flag]
    port, control = parseArguments()
    
    # Create server
    stop_event = threading.Event()      # Termination event
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    part1_pb2_grpc.add_Part1ServicesServicer_to_server(ServicesPart1(stop_event),server)
    
    # Start server
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    stop_event.wait()   # stop_event to be triggered in termination method
    server.stop(None)
    
if __name__ == "__main__":
    
    # Definir o nível de logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()
