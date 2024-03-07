from photon import Photon
from photon.theme import Theme, Colors

from engine.events import EventManger
#Events
Events = EventManger()

#PhotonUI
app = Photon(theme=Theme(
    primary=Colors.BLUE,
    success=Colors.GREEN,
    warning=Colors.YELLOW,
    error =Colors.RED
))