GAME DESIGN DOCUMENT: SMART HANDS (Refactor v2.0)
Project: Operation Soddy-Daisy
Type: Text-Based Field Deployment Simulator
Engine: Python (Console/Terminal)
UI Style: Numbered Menu System (BIOS/Terminal Aesthetic)

I. DEVELOPMENT GOAL
Refactor the existing Python script to use a Menu-Driven Interface (Selecting 1, 2, 3...) instead of a text parser. The game must track specific boolean flags to determine if the player succeeds or fails at critical "Gate" moments.

II. GLOBAL TECHNICAL REQUIREMENTS
The Loop: The game runs in a while loop.

Screen Clearing: At the start of every new Phase or Menu refresh, clear the console (os.system('cls' or 'clear')) so the interface looks like a clean HUD.

Input Handling: Accept integers only. If the user types invalid input, reprint the menu.

State Management: Track the following boolean flags globally:

inventory_packed (Default: False)

drivers_verified (Default: False)

bridge_called (Default: False)

serials_logged (Default: False)

III. PHASE LOGIC & NARRATIVE SCRIPT
PHASE 0: HOME BASE (The Setup)
Narrative:

"LOCATION: HOME BASE (MURFREESBORO). TIME: MONDAY, 20:00. STATUS: You are at your desk. The gear is piled on the floor. OBJECTIVE: Verify the 'Tech Deck' before you sleep."

Menu Options:

[ACTION] Check Laptop Drivers

Logic: Set drivers_verified = True. Print: [SYSTEM] USB-to-Serial Controller Active on COM3.

[ACTION] Pack All Gear

Logic: Set inventory_packed = True. Print: [SYSTEM] Laptop, Console Cable, and Tools secured.

[TRAVEL] Go to Sleep / Depart for Site

Logic:

IF inventory_packed is False: BLOCK PROGRESS. Print: "You cannot leave without your tools."

IF inventory_packed is True: TRANSITION to Phase 1. (Note: Allow player to leave even if drivers_verified is False. This is a trap.)

PHASE 1: THE INFILTRATION (Parking Lot)
Narrative:

"LOCATION: SITE 404 - SODDY-DAISY, TN. TIME: 08:40 EST. STATUS: You are sitting in your rental car. The engine is ticking cool. OBJECTIVE: Establish comms with The Bridge before entering."

Menu Options:

[ACTION] Join Bridge Call

Logic: Set bridge_called = True. Print: [BRIDGE] "Dispatch here. We have you checked in. You are green to enter."

[ACTION] Check Inventory

Logic: Print list of items.

[TRAVEL] Enter Building

Logic:

IF bridge_called is False: GAME OVER. Print: "MISSION FAILED. You walked on site without checking in. The client cancelled the ticket."

IF bridge_called is True: TRANSITION to Phase 2.

PHASE 2: THE EXECUTION (Server Room)
Narrative:

"LOCATION: MDF ROOM. STATUS: Loud fans. Tangled cables. The air smells like ozone. OBJECTIVE: Swap the hardware."

Menu Options:

[ACTION] Scan Rack

Logic: Print: "It is a 2-Post Relay Rack. The cabling is a mess."

[ACTION] De-Install Legacy Hardware

Logic: Print: "Old device removed."

[ACTION] Rack & Stack New Gear

Logic: Print: "New hardware mounted. Power connected."

[ACTION] Connect Console (The Moment of Truth)

Logic:

IF drivers_verified is True: SUCCESS. Print: "Console Connected. Configuring Switch..." -> TRANSITION to Phase 3.

IF drivers_verified is False: GAME OVER. Print: "CRITICAL FAILURE. Your laptop does not recognize the console cable. You forgot to check the drivers at home. You cannot complete the work. You are fired."

PHASE 3: LOGISTICS (The Paperwork)
Narrative:

"LOCATION: SITE 404 - LOADING DOCK. STATUS: The technical work is done. The bureaucratic work remains."

Menu Options:

[ACTION] Log Serial Numbers

Logic: Set serials_logged = True. Print: "Serial numbers recorded in spreadsheet."

[ACTION] Ship Gear via FedEx

Logic: Print: "Package dropped off. Tracking number saved."

[FINISH] Close Ticket

Logic:

IF serials_logged is False: GAME OVER. Print: "MISSION FAILED. You shipped the old gear without recording the serials. The equipment is lost. The client is refusing to pay."

IF serials_logged is True: VICTORY. Print: "MISSION COMPLETE. Good work, Deliverator. Payment authorized."
