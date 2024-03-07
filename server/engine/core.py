from dataforge import database
from dataforge import config

from engine.events import EventManager

Config = config.Config("data/config.json")

Users = database.RuntimeDB("users", logging=False, runtime=True)
Channels = database.RuntimeDB("channels", logging=False, runtime=True)

Events = EventManager()
Packets = EventManager()

#create lobby channel
Channels.create(database.Item(name="lobby", password=None, users=[]))