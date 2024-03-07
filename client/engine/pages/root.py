from photon import Page
from photon.theme import Variants
from photon.components import NavBar, NavTab
from photon.keymap import get_key

class Root(Page):
    def __init__(self, app):
        self.app = app
        
        self.connect_nav = NavBar(app, "ByteIRC", variant=Variants.PRIMARY, auto_render=False,
            tabs = [
                NavTab("Connect", ["Ctrl+E", 5], "Connect"),
                NavTab("Actions", ["Ctrl+A", 1], "QuickActions"),
            ], large=False)
        
    def on_render(self, sc):
        page = type(self.app.page).__name__
            
        if page in ["Connect", "ConnectHelp"]:
            self.connect_nav.on_render(sc)
        
    def on_input(self, key):
        # print(key, get_key(key))
        page = type(self.app.page).__name__
            
        if page in ["Connect", "ConnectHelp"]:
            self.connect_nav.on_input(key)