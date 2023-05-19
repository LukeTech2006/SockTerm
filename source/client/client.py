from blessed import Terminal; from suffixes import *
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

recv = ""
while True:
    if recv[-4:] != "\\NUI": curLine = input(term.gold + '$ ').upper()
    s.send(pickle.dumps(curLine))
    recv = str(pickle.loads(s.recv(1024)))
    print(recv[:-4])
    if recv[-4:] == EOF: break
    elif recv[-4:] == ACK: s.send(pickle.dumps("ACK"))
