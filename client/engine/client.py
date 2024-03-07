import socket
import threading

from engine.packet import Encode, Decode
from engine.core import Events
    
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
        self.status_message = None
        
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.running = False
        
    def connect(self, host, user):
        if self.running:
            return
        
        try:
            self.status = State.CONNECTING
            self.conn.connect((host, 5773))
        
        except Exception as error:
            print(error)
            
            self.status = State.ERROR
            self.status_message = f"Connection failed:\n{error}"
            return

        self.running = True
        self.status_message = f"Authenticating"
        threading.Thread(target=self.read).start()
        
        self.write(Encode(id="auth", username=user))
 
    def read(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break
            except ConnectionResetError:
                self.status = State.DROPPED
                self.status_message = f"[-] {self.addr[0]} dropped: Connection reset by peer"
                break
            
            except ConnectionAbortedError:
                self.status = State.DROPPED
                self.status_message = f"[-] {self.addr[0]} dropped: Connection aborted"
                break
            
            except Exception as error:
                self.status = State.DROPPED
                self.status_message = f"[-] {self.addr[0]} dropped: {error}"
                break
            
            print(data.decode("utf-8"))
            
    def process_packet(self, packet):
        if packet.get("id") == None:
            Events.call("on_error", "Invalid packet")
            return
            
        try:
            r = Events.pcall(packet, self, packet)
            if r: self.write(r)
        except Exception as e:
            Events.call("on_error", f"[-] {self.addr[0]} caused an error at packet@{packet.get('id')}: {e}")
        
    def write(self, packet):
        try:
            if type(packet) == str:
                packet = packet.encode("utf-8")
                
            self.conn.send(packet)
        except Exception as error:
            Events.call("on_error", f"Failed to send packet: {error}")
            return
        
    def drop(self):
        self.status = State.DROPPED
        self.running = False
        
        
Client = ClientManager()