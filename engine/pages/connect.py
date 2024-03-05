from photon import Page
from photon.theme import Variants
from photon.components import Input

class Connect(Page):
    def __init__(self, app):
        self.app = app
        self.input = Input(app, "Server IP", width=20, callback=self.server_submit, auto_render=False)
        
    def on_render(self, sc):
        self.input.on_render(sc)
        
    def on_input(self, key):
        self.input.on_input(key)
        
    def server_submit(self, value):
        print(value)