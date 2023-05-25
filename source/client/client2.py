import threading
import queue
from blessed import Terminal
from suffixes import *
from pwinput import pwinput
import socket
import pickle
import sys

term = Terminal()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 60000))

newinput =  []
stop = threading.Event()
input_queue = queue.Queue()
response_queue = queue.Queue()
curLine = ''

response_section = ""

def input_thread():
    global curLine
    global newinput
    global stop
    input_queue.put("TIME")
    
    while True:
        if not response_queue.empty():
            inputtype = int(response_queue.get())
            if inputtype == 1:
                curLine = input(term.move(term.height - 1, 0) + term.gold + '$ ').upper()
                input_queue.put(curLine)
            elif inputtype == 2:
                curLine = input(term.move(term.height - 1, 0) + newinput[1]).upper()
                input_queue.put(curLine)
            elif inputtype == 3:
                curLine = pwinput(term.move(term.height - 1, 0) + newinput[1]).upper()
                input_queue.put(curLine)
        if stop.is_set(): sys.exit(0)

def print_thread():
    global newinput
    global s, stop
    response_section_height = term.height - 2  # Adjusted to leave space for user input
    response_section = term.home + term.clear + term.turquoise(term.center(r"""
███████╗ ██████╗  ██████╗██╗  ██╗████████╗███████╗██████╗ ███╗   ███╗     ██╗    ██████╗ 
██╔════╝██╔═══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ███║   ██╔═████╗
███████╗██║   ██║██║     █████╔╝    ██║   █████╗  ██████╔╝██╔████╔██║    ╚██║   ██║██╔██║
╚════██║██║   ██║██║     ██╔═██╗    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║     ██║   ████╔╝██║
███████║╚██████╔╝╚██████╗██║  ██╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║     ██║██╗╚██████╔╝
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝ ╚═════╝ 
SockTerm - The Simple™ TCP Terminal
""")) + "\n"
    recv = ''

    while True:
        if not input_queue.empty():
            cur_input = input_queue.get()
            s.send(pickle.dumps(cur_input))
            recv = str(pickle.loads(s.recv(1024)))

            inputtype = 1
            if recv.count(EOF):
                response_section += recv[:-4]
                stop.set()
            elif recv.count(ACK):
                s.send(pickle.dumps("ACK"))
                inputtype = 1
                response_section += recv[:-4] + "\n"
            elif recv.count(NUI):
                inputtype = 0
                response_section += recv[:-4] + "\n"
            elif recv.count(CUI) > 0:
                newinput = recv.split(CUI)
                inputtype = 2
                response_section += newinput[0] + "\n"
            elif recv.count(PUI) > 0:
                newinput = recv.split(PUI)
                inputtype = 3
                response_section += newinput[0] + "\n"

            if stop.is_set(): sys.exit(0)
            response_queue.put(inputtype)
            
            # Check if the response section height is exceeded and reset if necessary
            if response_section.count('\n') > response_section_height:
                response_section = response_section.split('\n', 1)[1]

            # Clear the terminal and print the response section and user input
            print(term.home + term.clear + response_section, end='')
            
            #Check for terminus

input_thread = threading.Thread(target=input_thread)
print_thread = threading.Thread(target=print_thread)

input_thread.start()
print_thread.start()

input_thread.join()
print_thread.join()
