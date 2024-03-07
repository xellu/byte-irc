import os
import threading
from dataforge import console

try:
    from engine import core, server
except Exception as error:
    console.error(f"Failed to initialize server engine")
    console.error(f"Error: {error}")
    os._exit(0)
    
threading.Thread(target=server.Listen).start()