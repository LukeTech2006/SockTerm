import socket, blessed, pickle, time, session, json
from _thread import *; from suffixes import *; from hashlib import sha256
term = blessed.Terminal()
configuredport = 60000
currentUsers = {}
availUsers = json.load(open('users.json'))

def closeConWithErr(message: str, s: socket):
    print(term.red + f"[SERVER/Error] {message}" + term.normal)
    s.close()
    return

def commandHandler(uid: int, command: str, socket: socket):
    feedback = False
    if command == "EXIT":
        print(term.lightblue + f"[SERVER/Info] Client #{uid} closed the connection." + term.normal)
        socket.send(pickle.dumps(term.orange + "Connection closed. Goodbye!" + term.normal + EOF))
        currentUsers[uid] = None
        quit()
    elif command == "WHOAMI":
        try: feedback = pickle.dumps(term.lightblue + f"You are Client #{uid} and are currently logged in as {currentUsers[uid][0]}." + term.normal + ACK)
        except TypeError: feedback = pickle.dumps(term.lightblue + f"You are Client #{uid} and are currently not logged in." + term.normal + ACK)
    elif command == "TIME":
        feedback = pickle.dumps(term.lightblue + f"It is {time.strftime('%H:%M:%S', time.localtime())} on {time.strftime('%d.%m.%Y', time.localtime())}" + term.normal + ACK)
    elif command == "LOGON":
        try:
            if currentUsers[uid] != None: return pickle.dumps(term.red + f"You are already logged in!" + term.normal + ACK)
            socket.send(pickle.dumps(term.lightblue + f"Beginning login procedure." + CUI + "Username: "))
            uname = pickle.loads(socket.recv(1024))
            socket.send(pickle.dumps(term.lightblue + PUI + term.move_up + "Password: "))
            pcode = sha256(pickle.loads(socket.recv(1024)).encode('utf-8')).hexdigest()
            if availUsers[uname] == pcode:
                feedback = pickle.dumps(term.green + f"Welcome, {uname}!" + term.normal + ACK)
                currentUsers[uid] = (uname, pcode)
            else: raise KeyError
        except KeyError: feedback = pickle.dumps(term.red + f"Unable to authenticate {uname or ''}!" + term.normal + ACK)
    elif command == "LOGOFF":
        if currentUsers[uid] == None: return pickle.dumps(term.red + f"You need to be logged in!" + term.normal + ACK)
        feedback = pickle.dumps(term.lightblue + f"Goodbye, {currentUsers[uid][0]}!" + term.normal + ACK)
        currentUsers[uid] = None

    return feedback

def clientHandler(s, a):
    global term
    uid = abs(hash(a))
    currentUsers[uid] = None
    print(term.lightblue + f"[SERVER/Info] Client at {a[0]}:{a[1]} is #{uid}." + term.normal)
    while True:
        try:
            s.settimeout(None)
            buf = s.recv(1024)
            feedback = commandHandler(uid, pickle.loads(buf), s)
            s.send(feedback or pickle.dumps(term.red + "Unknown command." + term.normal + ACK))
        
            #get acknowledgement from client, else fail
            s.settimeout(10)
            buf = s.recv(1024)
            if buf == pickle.dumps("ACK"): print(term.blue + f"[SERVER/Debug] Client #{uid} ACK" + term.normal)
            else: print(term.orange + f"[SERVER/Warning] Client #{uid} Non Standard ACK '{pickle.loads(buf)}'" + term.normal)
        except TimeoutError:
            closeConWithErr(f"Socket {a[1]} for Client #{uid} timed out. Connection closed!", s)
            currentUsers[uid] = None
            break
        except ConnectionResetError:
            closeConWithErr(f"Socket {a[1]} for Client #{uid} reset. Connection closed!", s)
            currentUsers[uid] = None
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