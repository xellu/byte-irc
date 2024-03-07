import time

from engine.core import Packets, Events, Users, Channels
from engine.packet import Encode

def send_message(channel, author, message):
    for c in Channels.content:
        if c.name == channel:
            for u in c.users:
                u.server.write(Encode(id="chat.message", channel=channel, author=author, message=message))
                return True
    return False

def announce_message(channel, message):
    for c in Channels.content:
        if c.name == channel:
            for u in c.users:
                u.server.write(Encode(id="chat.announce", channel=channel, author="*", message=message))
                return True
    return False

def send_error(server, message):
    server.write(Encode(id="chat.error", message=message))

@Packets.on("chat.message")
def chat_message(server, packet):
    if not server.user:
        return
    
    message = packet.get("message")
    if not message or type(message) != str:
        send_error(server, "Invalid message")
    if len(message) > 512:
        send_error(server, "Message too long")
    
    send_message(server.user.channel, server.user.username, message)
                
@Events.on("channel.join")
def channel_join(server, packet):
    if not server.user:
        return
    
    channel = Channels.find("name", packet.get("channel"))
    prev_channel = server.user.channel
    
    if prev_channel == packet.get("channel"):
        return Encode(id="chat.error", message="Already in channel")
    
    if not channel:
        return Encode(id="chat.error", message="Channel not found")
    
    if channel.password and packet.get("password") != channel.password:
        return Encode(id="chat.error", message="Invalid password")
    
    for c in Channels.content:
        if server.user in c.users:
            c.users.remove(server.user)
            if len(c.users) == 0:
                Channels.delete(c)
                    
    channel.users.append(server.user)
    server.user.channel = channel.name
    
    announce_message(channel.name, f"{server.user.username} joined the channel")
    announce_message(channel.name, f"{server.user.username} left the channel")
    
@Packets.on("channel.list")
def channel_list(server, packet):
    if not server.user:
        return
    
    channels = []
    for c in Channels.content:
        channels.append({"name": c.name, "locked": c.password != None})
        
    return Encode(id="channel.list", channels=channels)
    