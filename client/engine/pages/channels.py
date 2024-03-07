from photon import Page
from photon.components import Table, TableRow, Modal, Input, Text
from photon.theme import Variants

from engine.client import Client
from engine.packet import Encode

class Channels(Page):
    def __init__(self, app):
        self.app = app
        
        self.table = Table(app, sizeY=app.screenY-5, y=2, selected=0, on_click=self.on_click, headers=["Channel     ", "Locked"], variant=Variants.PRIMARY, auto_render=False)
        
        self.new_channel = (
            Input(app, "Channel Name", width=30, callback=self.create_channel, auto_render=False),
            False
        )
        
    def on_render(self, sc):
        rows = []
        for channel in Client.channels:
            rows.append(TableRow([channel.get("name"), "Locked" if channel.get("locked") else ""]))
            
        self.table.rows = rows
        self.table.on_render(sc)
        Text(self.app, "Press [Enter] to join a channel", y=self.app.screenY-1)
        Text(self.app, "or use [N] to create a new one", y=self.app.screenY)
    
    def on_input(self, key):
        self.table.on_input(key)
    
    def on_click(self, index, row):
        Client.write(Encode(id="channel.join", channel=row.values[0]))
        
    def create_channel(self, value):
        if value.replace(" ", "") != "":
            Client.write(Encode(id="channel.create", name=value))
            self.new_channel = (self.new_channel[0], True)