import socket
import threading
import time

from engine.core import Config, Users, Events, Packets
from engine.packet import Encode, Decode

from dataforge import console

Info = console.tag(console.COLOR.LIGHTBLUE_EX, "Socket").print
Error = console.tag(console.COLOR.RED, "Socket", severity=console.Level.ERROR).print
Warn = console.tag(console.COLOR.YELLOW, "Socket", severity=console.Level.WARN).print

class ServerThread:
    def __init__(self, conn, addr):
        # console.error("created new server thread")
        
        self.conn = conn
        self.addr = addr
        
        self.auth_timeout = time.time() + 30
        self.user = None
        
        self.packet_queue = []
        self.running = True
        
    def read(self):
        while True:
            if not self.running: break
            
            try:
                data = self.conn.recv(1024)
                if not data:
                    self.drop("disconnected (no data)")
                    break
                
            except ConnectionResetError:
                self.drop("connection reset by peer")
                break
            
            except ConnectionAbortedError:
                self.drop("connection aborted")
                break
            
            except Exception as error:
                self.drop(f"exception: {error}")
                break
            
            packet = Decode(data)
            self.process_packet(packet)
            
    def process_packet(self, packet):
        if packet.get("id") == None:
            Error(f"[-] {self.addr[0]} sent invalid packet")
            return
        
        # if packet.get("id") not in ["heartbeat", "channel.list"]:
        #     Info(f"received: {packet}")
        
        if not self.user and packet.get("id") != "auth":
            self.write(Encode(id="auth", success=False, error="Authentication required"))
            return
            
        try:
            r = Packets.pcall(packet, self, packet)
            if r: self.write(r)
        except Exception as e:
            Error(f"[-] {self.addr[0]} caused an error at packet@{packet.get('id')}: {e}")

    def write(self, packet):
        if type(packet) == str:
            packet = packet.encode("utf-8")
            
        # if b"heartbeat" not in packet and b"channel.list" not in packet:
        #     print(f"writing: {packet}")
            
        self.conn.send(packet)

    def event_loop(self):
        while True:
            if not self.running: break
            
            if self.auth_timeout != 0 and time.time() > self.auth_timeout:
                self.write(Encode(id="auth", success=False, error="Failed to authenticate in time"))
                self.drop("authentication timeout")
            
            if self.user and self.user.last_heartbeat < time.time():
                self.write(Encode(id="auth", success=False, error="Connection timed out"))
                self.drop("timed out")
                
            for packet in self.packet_queue:
                # print(f"sending queued packet: {packet}")
                self.write(packet)
                self.packet_queue.remove(packet)
                
            time.sleep(0.25)
            
    def queue(self, packet):
        self.packet_queue.append(packet)

    def drop(self, reason=None):
        self.running = False
        self.conn.close()
        
        if self.user:
            Events.call("user.drop", self.user)
        
        user = self.addr[0]
        
        if reason:
            Info(f"[-] {user} dropped: {reason}")
            return
        
        Info(f"[-] {user} dropped")

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