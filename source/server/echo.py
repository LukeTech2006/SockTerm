import socket, blessed, pickle
from _thread import *; from suffixes import *
term = blessed.Terminal()
configuredport = 60000

def closeConWithErr(message: str, s: socket):
    print(term.red + f"[SERVER/Error] {message}" + term.normal)
    s.close()
    return

def commandHandler(uid: int, command: str, socket: socket):
    return False

def clientHandler(s, a):
    global term
    uid = abs(hash(a))
    print(term.lightblue + f"[SERVER/Info] Client at {a[0]}:{a[1]} is #{uid}." + term.normal)
    while True:
        try:
            s.settimeout(None)
            buf = s.recv(1024)
            if buf == pickle.dumps("CLOSE"):
                print(term.lightblue + f"[SERVER/Info] Client #{uid} closed the connection." + term.normal)
                s.send(pickle.dumps(term.lightblue + "Connection closed. Goodbye!" + term.normal + EOF))
                break
            else:
                feedback = commandHandler(uid, pickle.loads(buf), s)
                s.send(feedback or pickle.dumps(term.red + "Unknown command." + term.normal + ACK))
        
            #get acknowledgement from client, else fail
            s.settimeout(10)
            buf = s.recv(1024)
            if buf == pickle.dumps("ACK"): print(term.blue + f"[SERVER/Debug] Client #{uid} ACK" + term.normal)
            else: print(term.orange + f"[SERVER/Warning] Client #{uid} Non Standard ACK '{pickle.loads(buf)}'" + term.normal)
        except TimeoutError:
            closeConWithErr(f"Socket {a[1]} for Client #{uid} timed out. Connection closed!", s)
            break
        except ConnectionResetError:
            closeConWithErr(f"Socket {a[1]} for Client #{uid} reset. Connection closed!", s)
            break

print(term.home + term.clear + term.lightblue(term.center(r"""
███████╗ ██████╗  ██████╗██╗  ██╗███████╗███████╗██████╗ ██╗   ██╗███████╗     ██╗    ██████╗ 
██╔════╝██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝    ███║   ██╔═████╗
███████╗██║   ██║██║     █████╔╝ ███████╗█████╗  ██████╔╝██║   ██║█████╗      ╚██║   ██║██╔██║
╚════██║██║   ██║██║     ██╔═██╗ ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝       ██║   ████╔╝██║
███████║╚██████╔╝╚██████╗██║  ██╗███████║███████╗██║  ██║ ╚████╔╝ ███████╗     ██║██╗╚██████╔╝
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝     ╚═╝╚═╝ ╚═════╝ 
SockServe - The Simple™ TCP Server
""")))

print(term.lightblue + f"[SERVER/Info] Seting up TCP Socket for {socket.gethostname()} on port {configuredport}!")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), configuredport))
serversocket.listen(5)
print(f"[SERVER/Info] Setup complete. Now listening to network traffic.\n" + term.normal)

while True:
    (clientsocket, address) = serversocket.accept()
    print(term.lightblue + f"[SERVER/Info] Client connected from {address[0]} on port {address[1]}!" + term.normal)
    start_new_thread(clientHandler, (clientsocket, address, ))