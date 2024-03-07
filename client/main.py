from engine.core import app
from engine.pages import (root, connect, chat, quickactions, channels)
from engine.events import (events, auth, chat as chatEvent)

PAGES = [connect.Connect, chat.Chat, quickactions.QuickActions, channels.Channels]

app.root = root.Root(app)
for p in PAGES:
    app.register_page(p(app))

@app.event("on_error")
def on_error(source, error):
    print(f"Error from {type(source).__name__}: {error}")

app.open("Connect")
app.run()

#port 5773