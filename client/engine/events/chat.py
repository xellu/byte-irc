from engine.packet import Encode
from engine.core import Events

#channel packets----------------------------------------------------------------

@Events.on("channel.list")
def channel_list(client, packet):
    client.channels = packet.get("channels")
    client.current_channel = packet.get("current")

@Events.on("channel.join")
def channel_join(client, packet):
    if packet.get("success"):
        client.current_channel = packet.get("channel")
    
#chat packets-------------------------------------------------------------------
    
@Events.on("chat.message")
def chat_message(client, packet):
    # if not packet.get("author") or not packet.get("message"):
    #     return
    
    msg = f"{packet.get('author')}: {packet.get('message')}"
    
    client.chat.append({"content": msg, "type": "message"})
    if len(client.chat) > 512:
        client.chat = client.chat[-512:]
  
@Events.on("chat.system")
def chat_system(client, packet):
    client.chat.append({"content": f'* {packet.get("message")}', "type": packet.get("type")})
    if len(client.chat) > 512:
        client.chat = client.chat[-512:]