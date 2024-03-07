import socket
import threading
import socketserver

from engine.core import Config
from engine.packet import Encode, Decode

from dataforge import console

Info = console.tag(console.COLOR.LIGHTBLUE_EX, "Socket").print

class ServerThread:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        
    def read(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            
            print(data.decode("utf-8"))

    def event_loop(self):
        pass

def Listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Config.HOST, 5773))
        s.listen()

        Info("Socket server running, listening for connections")
        while True:
            conn, addr = s.accept()
            Info(f"{addr[0]}:{addr[1]} Connected")
            server = ServerThread(conn, addr)
            threading.Thread(target=server.read).start()
            threading.Thread(target=server.event_loop).start()