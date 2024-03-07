import time

from engine.core import Packets, Events, Users, Channels
from engine.packet import Encode

from dataforge.database import Item

@Packets.on("auth")
def auth(server, packet):
    user = str(packet.get("username"))
    
    if len(user) > 16:
        return Encode(id="auth", success=False, error="Username too long")
    
    if len(user) < 3:
        return Encode(id="auth", success=False, error="Username too short")
    
    if Users.find("username", user):
        return Encode(id="auth", success=False, error="User already exists")
    
    server.auth_timeout = 0
    
    u = Item(
        username = user,
        channel = ".",
        last_heartbeat = time.time() + 5,
        server = server
    )
    server.user = u
    Users.create(u)
    
    # Events.call("channel.join", server, {"channel": "lobby"})
    return Encode(id="auth", success=True, channel="lobby")

@Packets.on("heartbeat")
def heartbeat(server, packet):
    server.user.last_heartbeat = time.time() + 30
    
@Events.on("user.drop")
def user_drop(user):
    Users.delete(user)
    for c in Channels.content:
        if user in c.users:
            c.users.remove(user)
            Events.call("channel.announce", c.name, f"{user.username} left the channel")