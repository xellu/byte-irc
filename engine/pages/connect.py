from photon import Page
from photon.theme import Variants
from photon.components import Input


class Connect(Page):
    def __init__(self, app):
        self.app = app
        
        self.stage = "server"
        
        self.ip = ""
        self.user = ""
        
        self.server_address = Input(app, "Server Address", width=30, callback=self.server_submit, auto_render=False)
        self.username = Input(app, "Username", width=30, callback=self.username_submit, auto_render=False)
        
    def on_render(self, sc):
        match self.stage:
            case "server":
                self.server_address.on_render(sc)
            case "username":
                self.username.on_render(sc)
        
    def on_input(self, key):
        match self.stage:
            case "server":
                self.server_address.on_input(key)
            case "username":
                self.username.on_input(key)
        
    def server_submit(self, value):
        if value.replace(" ", "") != "":
            self.ip = value
            
        self.stage = "username"
        
    def username_submit(self, value):
        if value.replace(" ", "") != "":
            self.user = value
        
        