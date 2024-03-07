from photon import Page
from photon.theme import Variants
from photon.components import NavBar, NavTab
from photon.keymap import get_key

from engine.client import Client, State
class Root(Page):
    def __init__(self, app):
        self.app = app
        
        self.connect_nav = NavBar(app, "ByteIRC", variant=Variants.PRIMARY, auto_render=False,
            tabs = [
                NavTab("Connect", ["^E", 5], "Connect"),
                NavTab("Actions", ["^A", 1], "QuickActions"),
            ], large=False)
        
        self.main_nav = NavBar(app, "ByteIRC", variant=Variants.PRIMARY, auto_render=False,
            tabs = [
                NavTab("Chat", ["^T", 20], "Chat"),
                NavTab("Channels", ["^F", 6], "Channels"),
                NavTab("Actions", ["^A", 1], "QuickActions"),
            ], large=False)
        
    def on_render(self, sc):
        if Client.status == State.CONNECTED:
            self.main_nav.on_render(sc)
        else:
            self.connect_nav.on_render(sc)
        
    def on_input(self, key):
        print(key, get_key(key))
            
        if Client.status == State.CONNECTED:
            self.main_nav.on_input(key)
        else:
            self.connect_nav.on_input(key)