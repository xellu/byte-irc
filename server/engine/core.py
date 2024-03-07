from dataforge import database
from dataforge import config

Config = config.Config("data/config.json")
Users = database.RuntimeDB("users", logging=False)