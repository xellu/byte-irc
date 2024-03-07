import dataforge.core.commands as commands
import dataforge.database.engine as engine
import dataforge.database.logging as log
import dataforge.core.notification as notification
import os, json, time
import threading

Item = engine.item
instances = []

#DB
class RuntimeDB:
    def __init__(self, name, folder="data",  logging = True, debug = False, runtime=False):
        self.name = name
        self.folder = folder
        self.path = os.path.join(self.folder, self.name + ".xeldb")
        self.content = []
        self.logging = logging
        self.debug = debug
        self.runtime = runtime
        
        if os.path.exists(self.path) == False and runtime == False:
            open(self.path, "x").write("[]")
        
        self.load()
        instances.append(self)
        log.info("INSTANCE CREATED", db=self)
    
    #LOADING AND SAVING DATA
    def save(self, indent:bool = False):
        _save = []
        for x in self.content:
            _save.append( vars(x) )
        
        open(self.path, "w", encoding="utf-8").write(
            json.dumps( _save, indent=2 ) if indent else json.dumps( _save )
        )
        log.info(f"SAVE", db=self)
    
    def load(self):
        if self.runtime: return
        
        dataset = json.loads( open( self.path, "r", encoding="utf-8" ).read() )
        for data in dataset:
            i = Item()
            for x in data:
                setattr(i, x, data[x])
            
            self.content.append( i )
        log.info(f"LOAD", db=self)
            
    def wipe(self):
        os.remove(self.path)
        log.info(f"WIPE", db=self)
    
    #SEARCHING    
    def find(self, key, query):
        for item in self.content:
            if vars(item).get(key) == query:
                log.info(f"FIND: [{key}:{query}] (FOUND)", db=self)
                return item
            
        log.info(f"FIND: [{key}:{query}] (NOT FOUND)", db=self)
        
    def findall(self, key, query):
        output = []
        for item in self.content:
            if vars(item).get(key) == query:
                output.append( item )
        
        log.info(f"FINDALL: [{key}:{query}] ({len(output)} FOUND)", db=self)
        return output
    
    #MANAGEMENT
    def delete(self, item: Item):
        self.content.remove( item )
        log.info(f"ITEM DELETE: {item.DATAFORGE_UUID}", db=self)
    
    def remove(self, item: Item):
        self.delete(item)
        log.info(f"ITEM DELETE: {item.DATAFORGE_UUID}", db=self)
        
    def add(self, item: Item):
        self.content.append( item )
        log.info(f"ITEM ADD: {item.DATAFORGE_UUID}", db=self)
        return item
    
    def create(self, item: Item):
        self.add(item)
        log.info(f"ITEM ADD: {item.DATAFORGE_UUID}", db=self)
        return item
        
    def clone(self, item: Item):
        item.DATAFORGE_UUID = engine._id()
        self.add(item)
        log.info(f"ITEM CLONE: {item.DATAFORGE_UUID}", db=self)
        return item

def get_instance(name):
    for x in instances:
        if x.name == name:
            return x
            
#HELP---
commands.register("database", "Database(name)", "Create a database instance")
commands.register("database", "Database.save([json indent:int])", "Saves database data to a <name>.xeldb file")
commands.register("database", "Database.load", "Loads database data from a file")
commands.register("database", "Database.wipe", "Deletes database file")
commands.register("database", "Database.find(key, query)", "Finds an item in the database matching the parameters")
commands.register("database", "Database.findall(key, query)", "Finds all items in the database matching the parameters")
commands.register("database", "Database.delete(item)", "Deletes an item from the database")
commands.register("database", "Database.remove(item)", "Deletes an item from the database")
commands.register("database", "Database.add(item)", "Creates an item and adds it to the database")
commands.register("database", "Database.create(item)", "Creates an item and adds it to the database")
commands.register("database", "Database.clone(item)", "Clones the item (will have different DataForge UUID)")
