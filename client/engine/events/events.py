from engine.core import Events

@Events.on("on_error")
def on_error(error):
    print(f"Error: {error}")