GAME DESIGN DOCUMENT: SMART HANDS (Refactor v2.0 + Level 2 Economy)
Project: Operation Soddy-Daisy
Type: Text-Based Field Deployment Simulator
Engine: Python (Console/Terminal)
UI Style: Numbered Menu System (BIOS/Terminal Aesthetic)

I. DEVELOPMENT GOAL
Refactor the existing Python script to use a Menu-Driven Interface (Selecting 1, 2, 3...) instead of a text parser. The game must track specific boolean flags to determine if the player succeeds or fails at critical "Gate" moments.
Implement Level 2 with a Global Economy system.

II. GLOBAL TECHNICAL REQUIREMENTS
The Loop: The game runs in a while loop.

Screen Clearing: At the start of every new Phase or Menu refresh, clear the console (os.system('cls' or 'clear')) so the interface looks like a clean HUD.

Input Handling: Accept integers only. If the user types invalid input, reprint the menu.

State Management: Track the following boolean flags globally:

inventory_packed (Default: False)
drivers_verified (Default: False)
bridge_called (Default: False)
serials_logged (Default: False)

New Variables (v2.1):
player_credits (Float). Starts at $0.00.
has_micro_driver (Bool). Default: False.
zoom_active (Bool). Default: False.

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
IF serials_logged is True: SUCCESS. TRANSITION to Phase 4 (Level 1 Closeout).

--- LEVEL 2 & ECONOMY UPDATE ---

PHASE 4: LEVEL 1 CLOSEOUT (The Payout)
Trigger: Completing "Operation Soddy-Daisy".
Action: Add $585.00 to player_credits.
Narrative: "Payment approved. Transferring $585.00 to account. 7-day terms active."
Transition: Go to PHASE 5 (The Hub).

PHASE 5: THE HUB (Intermission)
Narrative:
"DATE: THURSDAY, DEC 18. LOCATION: HOME OFFICE. BALANCE: $[Amount] ALERT: New Work Order Received for Friday 07:15 AM."

Menu:
[SHOP] Buy Micro-Screwdriver Set ($15.00)
Logic: Subtract $15. Set has_micro_driver = True.
[JOB] Read Level 2 Brief (Dell-Versa)
[ACCEPT] Deploy to Level 2
Logic:
IF has_micro_driver is False: Warning "You are accepting a job without the required tools. Risk is high." (Allow proceed, but trap them later). Transition to Phase 6.

PHASE 6: LEVEL 2 SITE (Arrival & Prep)
Narrative:
"LOCATION: OFFICE PARK. TIME: FRIDAY 07:15 AM. STATUS: The Client requires a Zoom video bridge for the entire swap. OBJECTIVE: Establish video link."

Menu:
[ACTION] Connect Laptop to Office Wi-Fi
Logic: TRAP. Print: "Connection Failed. The router you are here to replace is broken. You have no internet."
[ACTION] Boot Laptop + Connect Mobile Hotspot
Logic: CORRECT. Set zoom_active = True. Print: "Hotspot 5G Locked. Zoom Bridge Established. WSI Support is online."
[ACTION] Unplug Old Router Immediately
Logic: GAME OVER. Print: "FAILURE. You unplugged the device before the bridge was up. WSI Support has no eyes on the site. You are sent home."
[CONTINUE] Proceed to Swap (If Zoom Active) -> Transition to Phase 7.

PHASE 7: THE SWAP (The Tool Check)
Narrative:
"WSI SUPPORT: 'Okay tech, I see the device. Go ahead and open the chassis to swap the module.'"

Menu:
[ACTION] Use Standard Phillips Driver
Logic: FAILURE. Print: "The screws are too small. Your standard driver is stripping the head. You cannot open the chassis." -> GAME OVER (Marked as 'Unprepared').
[ACTION] Use Micro Phillips (Jeweler's Set)
Logic: (Requires has_micro_driver). SUCCESS. Print: "Smooth turn. Chassis open. Module swapped." Transition to Phase 8.

PHASE 8: NEGOTIATION (The Financials)
Narrative:
"TIME: 10:10 AM (3 Hour Mark). STATUS: The technical work is done, but WSI is running slow on their config. You are capped at 3 hours pay."

Menu:
[ACTION] Stay Silent & Finish
Logic: Job ends. Pay = $160. Transition to Victory.
[NEGOTIATION] Message Buyer: "Technical delays on your end. Requesting +1 Hour Overtime."
Logic: (RNG or Skill Check).
Success: Pay = $210 ($160 + $50). Print: "Buyer Approved. Overtime authorized."
Fail: Pay = $160. Print: "Buyer Denied. 'Stick to the cap.'"
Transition to Victory.

IV. NARRATIVE ASSETS (Level 2)
MSG_L2_BRIEF:
"WORK ORDER: Dell-Versa Router Swap. PAY: $160.00. WARNING: Unit uses proprietary micro-screws. DO NOT ARRIVE WITHOUT JEWELER'S TOOLS. PROCEDURE: Label all cables (WAN/LAN) before removal. WSI Support controls the show."

MSG_TOOL_FAIL:
"CRITICAL ERROR: You are staring at a 1.5mm screw with a standard #2 Phillips driver. It won't fit. You cannot complete the swap. The client asks why you didn't read the 'Critical Gotcha' list."

MSG_ZOOM_SUCCESS:
"You are live on Zoom. The WSI engineer can see your hands. He gives you the thumbs up to proceed."

MSG_PAYDAY:
"INVOICE SUBMITTED. Base Pay: $60.00 Hourly: $100.00 TOTAL: $160.00 ACCOUNT BALANCE UPDATED."
