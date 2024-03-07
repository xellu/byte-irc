import os

from photon import Page
from photon.components import Table, TableRow
from photon.theme import Variants

from engine.core import Events, app
from engine.client import Client, State

class QuickActions(Page):
    def __init__(self, app):
        self.app = app
        
        rows = [
            TableRow(["Connect"]),
            TableRow(["Settings"]),
            TableRow(["Disconnect"]),
            TableRow(["Exit"])
        ]
        self.menu = Table(app, headers=["Quick Actions"], selected=0, rows=rows, auto_render=False, variant=Variants.PRIMARY, on_click=self.callback)
        
    def on_render(self, sc):
        self.menu.on_render(sc)
        
    def on_input(self, key):
        self.menu.on_input(key)
        
    def callback(self, index, row):
        match row.values[0]:
            case "Connect":
                if Client.status == State.CONNECTED:
                    Client.drop()
                    Client.status_message = "Disconnected"
                
                self.app.open("Connect")
            case "Settings":
                self.app.open("Settings")
            case "Disconnect":
                if Client.status == State.CONNECTED:
                    Client.drop()
                    Client.status_message = "Disconnected"
                    
            case "Exit":
                Events.call("on_exit")
                self.app.exit()
                os._exit(0)