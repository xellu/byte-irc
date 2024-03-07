from photon import Page

class Root(Page):
    def __init__(self, app):
        self.app = app
        
    def on_render(self, sc):
        sc.addstr(0, 0, "Hello, world!")
        
    def on_input(self, key):
        return super().on_input(key)