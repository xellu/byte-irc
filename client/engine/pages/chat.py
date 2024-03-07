from photon import Page
from photon.keymap import get_key

class Chat(Page):
    def __init__(self, app):
        self.app = app
        
    def on_render(self, sc):
        sc.addstr(0, 0, "Chat")
        
    def on_input(self, key):
        if key == get_key("q"):
            self.app.open("Connect")