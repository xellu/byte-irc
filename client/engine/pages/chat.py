from photon import Page
from photon.keymap import get_key
from photon.components import SideBar, SideBarRow, Text, Modal
from photon.theme import Variants

from engine.client import Client
from engine.packet import Encode

text_varians = {
    "message": Variants.DEFAULT,
    
    "info": Variants.PRIMARY,
    "error": Variants.ERROR,
    "warn": Variants.WARNING,
    "success": Variants.SUCCESS
}

class Chat(Page):
    def __init__(self, app):
        self.app = app
        
        self.focus = 0
        self.focusable = ["chat", "channels"]
        
        self.chat_index = 0
        
        self.message = ""
        
        self.sidebar = SideBar(app, y=1, selected=2, auto_render=False)
        
        
        
    def on_render(self, sc):
        focus = self.focusable[self.focus]
        
        #render sidebar
        self.sidebar.items = [SideBarRow("  Channels  ", selectable=False)]
        for c in Client.channels:
            name = c.get("name")
            if len(name) > 12:
                name = name[:9] + "..."
            self.sidebar.items.append(SideBarRow(name))
        
        self.sidebar.variant = Variants.PRIMARY        
        if focus == "channels":
            self.sidebar.variant = Variants.DEFAULT

        
        self.sidebar.on_render(sc)
        
        #render message input
        msg = self.message if self.message else f"message #{Client.current_channel.get('name')}"
        if len(msg) > self.app.screenX-17:
            msg = msg[:self.app.screenX-17]
        
        Text(self.app, " "+msg.ljust(self.app.screenX-17), x=16, y=self.app.screenY, reverse=True,
            variant=Variants.DEFAULT if focus == "chat" else Variants.PRIMARY)
        
        #render chat
        startY = 2
        endY = self.app.screenY-1
        chat = Client.chat[-(endY-startY)+self.chat_index:]
        for i, line in enumerate(chat):
            Text(self.app, line.get("content"), y=startY+i, x=17, variant=text_varians.get(line.get("type"), Variants.DEFAULT))        
        
    def on_input(self, key):
        if get_key(key) == "tab":
            self.focus += 1
            if self.focus >= len(self.focusable):
                self.focus = 0
                
        focus = self.focusable[self.focus]
        
        match focus:
            case "chat":
                if get_key(key) == "backspace":
                    self.message = self.message[:-1]
                    return 
                
                elif get_key(key) == "enter":
                    if self.message:
                        Client.write(Encode(id="chat.message", message=self.message))
                        self.message = ""
                    return
                
                key = get_key(key)
                if len(key) != 1: return
                
                self.message += key
                
            case "channels":
                self.sidebar.on_input(key)