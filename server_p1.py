import argparse
import logging
import sys

log = logging.getLogger(__name__)

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

if __name__ == "__main__":
    
    # Definir o nível de logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()