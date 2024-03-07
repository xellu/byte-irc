import threading

from engine.core import Events, app
from engine.packet import Encode
from engine.client import State

@Events.on("auth")
def on_auth(client, packet):
    if packet.get("success"):
        #authed
        print("Successfully authenticated")
        
        client.status = State.CONNECTED
        client.status_message = "Connected"
        threading.Thread(target=client.event_loop).start()
    else:
        #auth failed/connection dropped
        Events.call("on_error", packet.get("error"))
        
        client.drop()
        client.status = State.ERROR
        client.status_message = packet.get("error")
        app.open("Connect")