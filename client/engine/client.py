import socket
import threading
import time
import json

from engine.packet import Encode, Decode
from engine.core import Events, app
    
class State:
    IDLE = "Idle"
    CONNECTING = "Connecting"
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    ERROR = "Error"
    DROPPED = "Connection Dropped"

class ClientManager:
    def __init__(self):
        self.status = State.IDLE
        self.status_message = "Idle"
        
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.running = False
        
        self.chat = []
        self.channels = []
        self.current_channel = "lobby"
                
    def connect(self, host, user):
        if self.running:
            return
        
        self.status_message = f"Connecting to {host}"
        
        try:
            self.status = State.CONNECTING
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            self.conn.connect((host, 5773))
        
        except Exception as error:
            Events.call("on_error", f"Connection attempt failed: {error}")
            
            self.status = State.ERROR
            self.status_message = str(error)
            self.drop()
            return

        self.running = True
        self.status_message = f"Authenticating"
        threading.Thread(target=self.read).start()
        
        self.write(Encode(id="auth", username=user))
 
    def read(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
            except ConnectionResetError:
                self.status = State.DROPPED
                self.status_message = f"Dropped: Connection reset by peer"
                Events.call("on_error", self.status_message)
                self.drop()
                break
            
            except ConnectionAbortedError:
                self.status = State.DROPPED
                self.status_message = f"Dropped: Connection aborted"
                Events.call("on_error", self.status_message)
                self.drop()
                break
            
            except Exception as error:
                self.status = State.DROPPED
                self.status_message = f"Dropped: {error}"
                Events.call("on_error", self.status_message)
                self.drop()
                break
            
            try:
                packet = Decode(data)
                self.process_packet(packet)
            except Exception as error:
                Events.call("on_error", f"Failed to decode packet: {error}")
            
    def process_packet(self, packet):
        if packet.get("id") == None:
            Events.call("on_error", "Invalid packet")
            return
            
        try:
            r = Events.pcall(packet, self, packet)
            if r: self.write(r)
        except Exception as e:
            Events.call("on_error", f"[-] Caused an error at packet@{packet.get('id')}: {e}")
        
    def write(self, packet):
        try:
            if type(packet) == str:
                packet = packet.encode("utf-8")
                
            print(f"Sending {json.loads(packet.decode('utf-8')).get('id')}")
            self.conn.send(packet)
        except Exception as error:
            Events.call("on_error", f"Failed to send packet: {error}")
            return
        
    def event_loop(self):
        next_heartbeat = 0
        while self.running:
            if not self.running: break
            
            if next_heartbeat < time.time():
                self.write(Encode(id="heartbeat", timestamp=time.time()))
                self.write(Encode(id="channel.list"))
                next_heartbeat = time.time() + 10
        
    def drop(self):
        self.status = State.DROPPED
        self.running = False
        
        app.open("Connect")
        
        try:
            self.conn.close()
        except: pass
        
        
Client = ClientManager()