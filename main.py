from photon import Photon

from engine.pages import (root, connect)

app = Photon(root=root.Root)
PAGES = [connect.Connect]

for p in PAGES:
    app.register_page(p(app))
    
app.open("Connect")
app.run()