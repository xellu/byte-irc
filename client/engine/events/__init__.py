class EventManger:
    def __init__(self):
        self.events = {}
    
    def on(self, event):
        def wrapper(func):
            self.events[event] = func
            return func
        
        return wrapper
    
    def pcall(self, packet, *args, **kwargs):
        packet_id = packet.get("id")
        if packet_id in self.events:
            return self.events[packet_id](*args, **kwargs)
        else:
            print(f"No event for packet {packet_id}")
            
    def call(self, event, *args, **kwargs):
        if event in self.events:
            self.events[event](*args, **kwargs)
        else:
            print(f"No event for {event}")