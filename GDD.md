REFACTOR INSTRUCTION: SWITCH TO MENU-DRIVEN UI
Context: We are updating the "Smart Hands" Python game engine. Currently, it uses a text parser (typing verbs). We need to refactor the entire input loop to use a Numbered Multiple Choice System.

Objective: Replace input("> ") text parsing with a dynamic menu system where the player selects an action by typing a number (1, 2, 3...).

I. NEW UI LAYOUT (Standard Format)
For every "Game State" or "Location," the console must print:

The Narrative/Status: (e.g., "You are at Home Base...")

The Options List: A generated list of valid actions for that specific state.

The Prompt: Select Option [1-3]:

II. PHASE-SPECIFIC MENU LOGIC
Phase 0: Home Base
Narrative: "LOCATION: HOME BASE (MURFREESBORO). TIME: MONDAY, 20:00. Verify your Tech Deck." Menu Options:

[ACTION] Check Laptop Drivers (Sets drivers_verified = True)

[ACTION] Pack All Gear (Sets inventory_full = True)

[TRAVEL] Go to Sleep / Depart for Site (Triggers Phase 1 Transition)

Logic Check (The "Lazy Tech" Trap):

If player selects 3 without doing 1, store a hidden flag driver_failure = True. Do NOT stop them. Let them fail later.

If player selects 3 without doing 2, block progress: "You cannot leave without your tools."

Phase 1: The Parking Lot
Narrative: "LOCATION: SITE 404. TIME: 08:40. You are in the car." Menu Options:

[ACTION] Join Bridge Call (Sets bridge_comms = True)

[ACTION] Check Inventory

[TRAVEL] Enter Building (Triggers Phase 2 Transition)

Logic Check:

If player selects 3 without doing 1, trigger specific failure text: "You walked in without calling the Bridge. They are angry. Mission Failed."

Phase 2: The Server Room
Narrative: "LOCATION: MDF ROOM. Loud fans. Tangled cables." Menu Options:

[ACTION] Scan Rack (Reads descriptions)

[ACTION] De-Install Legacy Hardware

[ACTION] Rack & Stack New Gear (Requires drivers_verified == True)

[ACTION] Connect Console (The Moment of Truth)

Logic Check (The Reveal):

When selecting 4:

If drivers_verified == True: Success message ("Console Connected via COM3").

If drivers_verified == False: GAME OVER. ("Error: Driver not found. You are stuck on site with no way to work. You are fired.")

Phase 3: Logistics & Closeout
Narrative: "Job done. Cleanup time." Menu Options:

[ACTION] Log Serial Numbers (Sets serials_logged = True)

[ACTION] Ship Gear via FedEx

[ACTION] Get Client Signature

[FINISH] Depart Site

III. TECHNICAL REQUIREMENTS
Loop: The game should loop and clear the screen (optional) between choices so the menu is always fresh.

Error Handling: If the user types "5" when there are only 3 options, print "Invalid Selection" and show the menu again.

State Persistence: Ensure boolean flags (drivers, inventory, comms) carry over between menu selections.

