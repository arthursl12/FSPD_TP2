#!/usr/bin/env python

import argparse
import logging
import sys
from concurrent import futures  # for thread pool

import grpc

import part1_pb2
import part1_pb2_grpc

log = logging.getLogger(__name__)
stored = {}
class ServicesPart1(part1_pb2_grpc.Part1ServicesServicer):

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
        print(f"GRPC server in consult, ch={request.integer}")
        return part1_pb2.ConsultReply(ch=10, s="teste")
    
    def activate(self, request, context):
        print(f"GRPC server in activate, s={request.s}")
        return part1_pb2.IntReply(ret_integer=0)
    
    def terminate(self, request, context):
        print(f"GRPC server in terminate")
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
    
    # Start server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    part1_pb2_grpc.add_Part1ServicesServicer_to_server(ServicesPart1(),server)
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    
    # Definir o nível de logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()
