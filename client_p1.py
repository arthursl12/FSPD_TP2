import argparse
import logging
import sys

log = logging.getLogger(__name__)

SEPARATOR = ','

def parseArguments():
    # Parsing dos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("id_servico", help="IP:porta do ponto do servidor")
    args = parser.parse_args()
    
    # Trata o IP e a porta
    ip_porta = str(args.id_servico)
    log.debug(f"Conectaremos a {ip_porta}")
    return ip_porta

def main():
    # Usage: python client_p1.py <IP:port>
    ip_porta = parseArguments()
    
    # Reading commands from standard input
    # (can be redirected from a file via "<" in terminal)
    for line in sys.stdin:
        line = ''.join(line.split())    # Remove all whitespaces from string
        # log.debug(f"Read: {line};")
        
        # Parsing commands
        if (line[0] == 'I'):
            _, ch, dest = line.split(SEPARATOR)
            ch = int(ch)
            log.debug(f"Insert: {ch} at {dest}")
        elif (line[0] == 'A'):
            _, dest = line.split(SEPARATOR)
            log.debug(f"Activate: {dest}")
        elif (line[0] == 'C'):
            _, ch = line.split(SEPARATOR)
            ch = int(ch)
            log.debug(f"Check: {ch}")
        elif (line[0] == 'T'):
            log.debug(f"Terminate")
            exit()
        else:
            log.debug(f"Unknown command: {line};")
        
        
        
        
    log.debug(f"Finished reading")
        

if __name__ == "__main__":
    
    # Definir o nível de logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    # logging.basicConfig()
    
    main()