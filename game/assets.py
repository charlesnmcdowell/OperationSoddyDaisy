"""
Narrative assets (String Database) for Smart Hands.
"""

LOC_HOME_BASE = """LOCATION: HOME BASE (MURFREESBORO).
TIME: MONDAY, 20:00.
STATUS: You are at your desk. The gear is piled on the floor.
OBJECTIVE: Verify the 'Tech Deck' before you sleep. If the drivers fail tomorrow, you don't get paid."""

LOC_PARKING_LOT = """LOCATION: SITE 404 - SODDY-DAISY, TN.
TIME: 08:40 EST.
STATUS: You are sitting in your rental car. The engine is ticking cool. Outside, the warehouse is a grey monolith against a grey sky.
OBJECTIVE: Establish comms with The Bridge before 08:45."""

LOC_SITE_ENTRANCE = """LOCATION: SITE ENTRANCE.
STATUS: You are at the security desk. A guard looks at you indifferently.
OBJECTIVE: Proceed to the Server Room."""

LOC_SERVER_ROOM = """LOCATION: SERVER ROOM.
STATUS: The hum of cooling fans fills the air. It's cold. 
RACK 1 contains the LEGACY_SWITCH.
OBJECTIVE: Swap the legacy gear for the NEW_SWITCH."""

LOC_FEDEX = """LOCATION: FEDEX DROP-OFF.
STATUS: A strip mall storefront. The clerk is chewing gum.
OBJECTIVE: Ship the legacy hardware."""

MSG_DRIVER_SUCCESS = """SYSTEM CHECK...
[OK] USB-to-Serial Controller detected on COM3.
[OK] Baud Rate: 9600.
READY FOR CONNECTION."""

MSG_DRIVER_FAIL = """SYSTEM CHECK...
[ERROR] DEVICE NOT RECOGNIZED.
[FATAL] You cannot interface with the client hardware.
MISSION FAILED: The Client has noticed your delay."""

MSG_HOTSPOT_CONNECT = """DEPLOYING HOTSPOT...
SIGNAL: LTE (2 Bars).
VPN TUNNEL: ESTABLISHED.
You are now on the corporate network."""

NPC_BRIDGE_INTRO = """BRIDGE: 'Tech, this is Dispatch. Do I have you on the line? We are on a hard start. Confirm when you are inside the facility.'"""

MSG_CONSOLE_CONNECT = """CONNECTING...
...
User Access Verification
Password:
> *******
> enable
> #
CONSOLE ESTABLISHED."""

MSG_MISSION_SUCCESS = """MISSION COMPLETE.
All objectives met.
The Bridge confirms green status.
You can go home."""

MSG_MISSION_FAIL = """MISSION FAILED.
You missed a critical step."""

