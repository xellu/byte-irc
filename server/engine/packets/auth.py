import time

from engine.core import Events, Users
from engine.packet import Encode

from dataforge.database import Item

@Events.on_packet("auth")
def auth(server, packet):
    user = str(packet.get("username"))
    
    if len(user) > 16:
        return Encode(id="auth", success=False, error="Username too long")
    
    if len(user) < 3:
        return Encode(id="auth", success=False, error="Username too short")
    
    if Users.find("username", user):
        return Encode(id="auth", success=False, error="User already exists")
    
    server.auth_timeout = None
    server.user = user
    
    u = Item(
        username = user,
        channel = None,
        last_heartbeat = time.time() + 60,
    )
    Users.create(u)
    
    return Encode(id="auth", success=True, channel=None)