import time

from engine.core import Packets, Events, Users, Channels
from engine.packet import Encode

from dataforge import console

def send_message(channel, author, message):
    for c in Channels.content:
        if c.name == channel:
            for u in c.users:
                u.server.queue(Encode(id="chat.message", channel=channel, author=author, message=message))

def announce_message(channel, message):
    for c in Channels.content:
        if c.name == channel:
            for u in c.users:
                u.server.queue(Encode(id="chat.system", type="info", message=message))

def global_announce(message):
    for u in Users.content:
        u.server.queue(Encode(id="chat.system", type="info", message=message))

def send_error(server, message):
    server.write(Encode(id="chat.system", type="error", message=message))

#events---------

@Events.on("channel.announce")
def channel_announce(channel, message):
    announce_message(channel, message)

@Events.on("global.announce")
def global_msg(message):
    global_announce(message)

#chat packets---------

@Packets.on("chat.message")
def chat_message(server, packet):
    if not server.user:
        send_error(server, "You are not authenticated")
        return
    
    if server.user.channel == ".":
        send_error(server, "You are not in a channel")
        return
    
    message = packet.get("message")
    if not message or type(message) != str:
        send_error(server, "Invalid message")
        return
    if len(message) > 512:
        send_error(server, "Message too long, maximum of 512 characters is allowed")
        return
    
    send_message(server.user.channel, server.user.username, message)
        
#channel packets---------
                
@Packets.on("channel.join")
def channel_join(server, packet):
    if not server.user:
        return
    
    channel = Channels.find("name", packet.get("channel"))
    prev_channel = server.user.channel
    
    if prev_channel == packet.get("channel"):
        return Encode(id="channel.join", message="Already in channel")
    
    if not channel:
        return Encode(id="channel.join", message="Channel not found")
    
    if channel.password and packet.get("password") != channel.password:
        return Encode(id="channel.join", message="Invalid password")
    
    for c in Channels.content:
        if server.user in c.users:
            c.users.remove(server.user)
            if len(c.users) == 0 and c.name != "lobby":
                console.warn(f"channel {c.name} was deleted: empty")
                Channels.delete(c)
                    
    channel.users.append(server.user)
    server.user.channel = channel.name
    
    announce_message(channel.name, f"{server.user.username} joined the channel")
    announce_message(prev_channel, f"{server.user.username} left the channel")
    return Encode(id="channel.join", channel=channel.name)
    
@Packets.on("channel.list")
def channel_list(server, packet):
    if not server.user:
        return
    
    channels = []
    for c in Channels.content:
        channels.append({"name": c.name, "locked": c.password != None})
        
    current = Channels.find("name", server.user.channel)
    if not current:
        Packets.call("channel.join", server, {"channel": "lobby"})
        current = Channels.find("name", "lobby")

    current = {"name": current.name, "locked": current.password != None, "users": len(current.users)}
        
    return Encode(id="channel.list", channels=channels, current=current)
    