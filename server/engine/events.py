from dataforge import console

Say = console.tag(console.COLOR.LIGHTCYAN_EX, "Events").print
Warn = console.tag(console.COLOR.YELLOW, "Events", severity=console.Level.WARN).print

class EventManager:
    def __init__(self):
        self.events = {}
        
    def on(self, packet_id):
        def wrapper(func):
            self.events[packet_id] = func
            return func
        
        return wrapper
    
    def pcall(self, packet, *args, **kwargs):
        packet_id = packet.get("id")
        if packet_id in self.events:
            return self.events[packet_id](*args, **kwargs)
        else:
            Warn(f"No event for packet {packet_id}")
            
    def call(self, event, *args, **kwargs):
        if event in self.events:
            self.events[event](*args, **kwargs)
        else:
            Warn(f"No event for {event}")