from blessed import Terminal; from suffixes import *; from pwinput import pwinput
import socket, pickle
term = Terminal()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 60000))

print(term.home + term.clear + term.turquoise(term.center(r"""
███████╗ ██████╗  ██████╗██╗  ██╗████████╗███████╗██████╗ ███╗   ███╗     ██╗    ██████╗ 
██╔════╝██╔═══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ███║   ██╔═████╗
███████╗██║   ██║██║     █████╔╝    ██║   █████╗  ██████╔╝██╔████╔██║    ╚██║   ██║██╔██║
╚════██║██║   ██║██║     ██╔═██╗    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║     ██║   ████╔╝██║
███████║╚██████╔╝╚██████╗██║  ██╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║     ██║██╗╚██████╔╝
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝ ╚═════╝ 
SockTerm - The Simple™ TCP Terminal
""")))

inputtype = 0
curLine = "TIME"
recv = ""
while True:
    if inputtype == 1: curLine = input(term.gold + '$ ').upper()
    if inputtype == 2: curLine = input(newinput[1]).upper()
    if inputtype == 3: curLine = pwinput(newinput[1]).upper()
    s.send(pickle.dumps(curLine))
    recv = str(pickle.loads(s.recv(1024)))
    
    inputtype = 1
    if recv[-4:] == EOF:
        print(recv[:-4])
        quit()
    elif recv[-4:] == ACK:
        s.send(pickle.dumps("ACK"))
        print(recv[:-4])
    elif recv[-4:] == NUI:
        inputtype = 0
        print(recv[:-4])
    elif recv.count(CUI) > 0:
        newinput = recv.split(CUI)
        inputtype = 2
        print(newinput[0])
    elif recv.count(PUI) > 0:
        newinput = recv.split(PUI)
        inputtype = 3
        print(newinput[0])