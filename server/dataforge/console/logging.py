from colorama import Fore
import time
import os

class Logger:
    def __init__(self):
        self.memory = []
        self.active = False
        self.replace_colors = vars(Fore)
        self.path = None
        
        self.running = True
        
    def set_path(self, path):
        self.path = path
    
    def start(self):
        self.memory = []
        self.active = True
        
        self.report("Logging", "-----------------------------------", "info")
        self.report("Logging", "      Logging process started      ", "info")
        self.report("Logging", "-----------------------------------", "info")
        
    def stop(self):     
        self.report("Logging", "-----------------------------------", "info")
        self.report("Logging", "      Logging process stopped      ", "info")
        self.report("Logging", "-----------------------------------", "info")

        self.running = False
        self.active = False

        self.save()

        
    def pause(self):
        self.active = False
    
    def resume(self):
        self.active = True
        
    def report(self, origin, message, severity):
        if self.active:
            _log = f"[{time.strftime('%d-%m-%y %H:%M:%S', time.localtime())}] [{severity.upper()}] {origin.upper()}: {message}"
            
            self.memory.append(_log)
            
    def save(self):
        if self.memory == []: return
        
        if not os.path.exists(self.path):
            open(self.path, "w", encoding="utf-8").write( "\n".join(self.memory) )
        else:    
            open(self.path, "a", encoding="utf-8").write( "\n" + "\n".join(self.memory) )
        self.memory = []
           
    def auto_update(self, interval=3):
        while self.running:
            time.sleep(interval)
            self.save()
            
    def get(self, index:int = None):
        if index == None:
            return self.memory

        return self.memory[index]