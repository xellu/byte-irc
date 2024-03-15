from photon import Page
from photon.components import Table, TableRow, Modal, Input, Text
from photon.theme import Variants
from photon.keymap import get_key

from engine.client import Client
from engine.packet import Encode

class Channels(Page):
    def __init__(self, app):
        self.app = app
        
        self.table = Table(app, sizeY=app.screenY-5, y=2, selected=0, on_click=self.on_table_click, headers=["Channel     ", "Locked"], variant=Variants.PRIMARY, auto_render=False)
        
        self.new_channel = {
            "name": "",
            "password": "",
            "stages": ["name", "password"],
            "index": 0,
            
            "name.form": Input(self.app, "Channel Name", callback=self.on_new_channel, auto_render=False),
            "password.form": Input(self.app, "Password (optional)", callback=self.on_new_channel, auto_render=False)
        }
        
        self.page = "list"
        
    def on_render(self, sc):
        #channel list
        if self.page == "list":
            rows = []
            for channel in Client.channels:
                rows.append(TableRow([channel.get("name"), "Locked" if channel.get("locked") else ""]))
                
            self.table.rows = rows
            self.table.on_render(sc)
            Text(self.app, "Press [Enter] to join a channel", y=self.app.screenY-1)
            Text(self.app, "or use [N] to create a new one", y=self.app.screenY)
            return
        
        #create channel
        self.new_channel[str(self.new_channel["stages"][self.new_channel["index"]])+".form"].on_render(sc)
            
            
                
    def on_input(self, key):
        if self.page == "list": #channel list
            if get_key(key).lower() == "n":
                self.page == "create"
                return
            
            self.table.on_input(key)
            return
            
        #create channel
        if get_key(key) == "esc":
            self.page == "list"
            return
        
        #manage stages
        if get_key(key) == "left":
            if self.index > 0:
                self.index -= 1
            return    
            
        if get_key(key) == "right":
            if self.index - 1 > len(self.stages):
                self.index += 1
            return
        
        #manage input
        self.new_channel[str(self.new_channel["stages"][self.new_channel["index"]])+".form"].on_input(key)
    
    def on_table_click(self, index, row):
        Client.write(Encode(id="channel.join", channel=row.values[0]))
        
    def on_new_channel(self, value):
        pass