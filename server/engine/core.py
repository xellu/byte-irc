from dataforge import database
from dataforge import config

from engine.events import EventManager

Config = config.Config("data/config.json")
Users = database.RuntimeDB("users", logging=False, runtime=True)

Events = EventManager()