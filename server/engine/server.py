import socket
import threading
import time

from engine.core import Config, Users, Events
from engine.packet import Encode, Decode

from dataforge import console

Info = console.tag(console.COLOR.LIGHTBLUE_EX, "Socket").print
Error = console.tag(console.COLOR.RED, "Socket", severity=console.Level.ERROR).print
Warn = console.tag(console.COLOR.YELLOW, "Socket", severity=console.Level.WARN).print

class ServerThread:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        
        self.auth_timeout = time.time() + 60
        self.user = None
        
        self.running = True
        
    def read(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if not data:
                    Info(f"[-] {self.addr[0]} disconnected")
                    break
                
            except ConnectionResetError:
                Info(f"[-] {self.addr[0]} dropped: Connection reset by peer")
                break
            
            except ConnectionAbortedError:
                Info(f"[-] {self.addr[0]} dropped: Connection aborted")
                break
            
            except Exception as error:
                Info(f"[-] {self.addr[0]} dropped: {error}")
                break
            
            packet = Decode(data)
            self.process_packet(packet)
            
        Warn(f"Connection aborted for {self.addr[0]}")

    def process_packet(self, packet):
        if packet.get("id") == None:
            Error(f"[-] {self.addr[0]} sent invalid packet")
            return
            
        try:
            r = Events.pcall(packet, self, packet)
            if r: self.write(r)
        except Exception as e:
            Error(f"[-] {self.addr[0]} caused an error at packet@{packet.get('id')}: {e}")

    def write(self, packet):
        if type(packet) == str:
            packet = packet.encode("utf-8")
            
        self.conn.send(packet)

    def event_loop(self):
        while self.running:
            if self.auth_timeout != None and time.time() > self.auth_timeout:
                self.write(Encode(id="auth", success=False, message="Connection timed out"))
                self.running = False

def Listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Config.HOST, 5773))
        s.listen()

        Info("Socket server running, listening for connections")
        while True:
            conn, addr = s.accept()
            Info(f"[+] {addr[0]} Connected")
            server = ServerThread(conn, addr)
            threading.Thread(target=server.read).start()
            threading.Thread(target=server.event_loop).start()