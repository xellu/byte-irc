from photon import Page
from photon.keymap import get_key
from photon.components import SideBar, SideBarRow, Text, Modal

from engine.client import Client
from engine.packet import Encode

class Chat(Page):
    def __init__(self, app):
        self.app = app
        
        self.focus = "chat"
        
        self.message = ""
        self.chat = []
        self.channels = []
        self.current_channel = ""
        
        self.sidebar = SideBar(app, y=1, items=[], auto_render=False)
        
        
        
    def on_render(self, sc):
        self.sidebar.items = [SideBarRow(channel) for channel in self.channels]
        
    def on_input(self, key):
        pass