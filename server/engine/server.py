import socket
import threading
import socketserver

from engine.core import Config



class ServerThread:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

def Listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Config.HOST, Config.PORT))
        s.listen()

        Socket.print("Listening for connections")
        while True:
            conn, addr = s.accept()
            Socket.print(f"[+] New connection from {addr[0]}:{addr[1]}")
            serve = Server(conn, addr)
            threading.Thread(target=serve.read).start()
            threading.Thread(target=serve.event_loop).start()