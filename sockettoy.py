import socket
from time import sleep

VDIVS = 12
HOST = '127.0.0.1'
PORT = 2224

def main():
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT))

    running = 1
    hello = 0
    
    while running:
        hello += 1
        tsr += 'test ' + str(hello) + '; '
        s2.send(tsr.encode())
        hello %= 100
        print tsr
        sleep(.5)
        

if __name__ == '__main__':
    main()
