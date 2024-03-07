from engine.core import app
from engine.pages import (root, connect, chat)
from engine.events import (events, auth)

PAGES = [connect.Connect, chat.Chat]

app.root = root
for p in PAGES:
    app.register_page(p(app))

app.open("Connect")
app.run()

#port 5773