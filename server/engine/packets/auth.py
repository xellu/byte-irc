import time

from engine.core import Events, Users
from engine.packet import Encode

from dataforge.database import Item

@Events.on("auth")
def auth(server, packet):
    user = str(packet.get("username"))
    
    if len(user) > 16:
        return Encode(id="auth", success=False, error="Username too long")
    
    if len(user) < 3:
        return Encode(id="auth", success=False, error="Username too short")
    
    if Users.find("username", user):
        return Encode(id="auth", success=False, error="User already exists")
    
    server.auth_timeout = None
    
    u = Item(
        username = user,
        channel = None,
        last_heartbeat = time.time() + 5,
        server = server
    )
    server.user = u
    Users.create(u)
    
    return Encode(id="auth", success=True, channel=None)

@Events.on("heartbeat")
def heartbeat(server, packet):
    server.user.last_heartbeat = time.time() + 30