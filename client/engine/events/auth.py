from engine.core import Events, app
from engine.packet import Encode
from engine.client import State

@Events.on("auth")
def on_auth(client, packet):
    if packet.get("success"):
        print("Successfully authenticated")
        client.status = State.CONNECTED
        
    else:
        Events.call("on_error", packet.get("error"))
        
        client.drop()
        client.status = State.ERROR
        client.status_message = packet.get("error")
        app.open("Connect")