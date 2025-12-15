# GAME DESIGN DOCUMENT: SMART HANDS

**Version:** 1.0 (MVP - Text Engine)
**Studio:** Deliverator Games
**Project Codename:** Operation Soddy-Daisy

## I. HIGH CONCEPT

Smart Hands is a high-stakes "Field Deployment" simulator where the player assumes the role of a remote operative (The Deliverator). The goal is to execute a complex technical installation in a hostile environment (a site with no internet/tools) under strict time pressure.

Unlike chaotic party games, the core tension here comes from competence. The horror isn't a monster; it's forgetting a serial number driver or missing a client signature.

## II. GAMEPLAY MECHANICS

### A. The Core Loop
1. **Prep (Base):** Validate loadout. (Failure here = Mission Fail).
2. **Deploy (Travel):** Manage strict ETA windows (Simulated via time deduction).
3. **Execute (Site):** Physical installation (Rack & Stack) + Software Config (Console/Putty).
4. **Exfil (Closeout):** The "Boss Fight" against documentation.

### B. The Loadout System (Inventory)
- **Critical Items:** Laptop (Win 11), Console Cable, Mobile Hotspot.
- **Hardware:** Monitor, drills, cage nuts, 5x Cat6 Cables.
- **Armor:** PPE (Vest, Boots, Hard Hat).
- **Mechanic:** "Hard Lock" - If the player arrives on-site without a Critical Item, the mission ends instantly.

### C. Mission Phases (Level Design)
- **Phase 0:** Pre-Deployment Stress Test (Driver verification at home).
- **Phase 1:** Infiltration (GPS Check-in & Bridge Call from the Parking Lot).
- **Phase 2:** The Grind (De-install legacy gear $\rightarrow$ Install new gear).
- **Phase 3:** Logistics (FedEx run).
- **Phase 4:** Documentation (Uploads & Sign-off).

## III. WIN / LOSS CONDITIONS

### Victory Conditions
To clear the level, the player must have:
- Hardware installed and confirmed "Green" by the Bridge.
- Old gear logged and "shipped" (Player has the tracking number).
- Sign-off sheet physically signed by the Site Contact.
- All documentation uploaded.

### Game Over States
- **The Driver Error:** Player fails to verify USB-to-Serial drivers before leaving Base. Result: Cannot console into the switch.
- **The Ghost Error:** Player leaves the site without recording Serial Numbers of old gear. Result: Cannot complete shipping manifest.
- **The Abandonment:** Player exits the location without the client signature. Result: Pay withheld.

## IV. TECHNICAL SPECIFICATIONS

- **Target Platform:** PC (Command-Line Interface / Terminal).
- **Engine:** Python (Text-based).
- **Visual Style:** "Terminal Aesthetic" (Green text on Black background). Monospaced fonts.
- **Input:** Text Parser (Verb-Noun).

## V. COMMAND SYNTAX (CONTROLS)

The parser should recognize these specific "Engineering Verbs."

### 1. Diagnostic (Looking)
- `SCAN [TARGET]` (e.g., SCAN RACK, SCAN LAPTOP, SCAN ROOM)
- `CHECK [STATUS]` (e.g., CHECK TIME, CHECK DRIVER, CHECK SIGNAL)
- `LIST INVENTORY`

### 2. Action (Doing)
- `DEPLOY [ITEM]` (e.g., DEPLOY HOTSPOT, DEPLOY MONITOR)
- `CONNECT [CABLE] TO [PORT]` (e.g., CONNECT CONSOLE TO SWITCH)
- `TYPE [COMMAND]` (e.g., TYPE IPCONFIG)

### 3. Logistics (Bureaucracy)
- `MOVE [LOCATION]` (e.g., MOVE TO SERVER_ROOM)
- `LOG [ITEM]` (e.g., LOG SERIAL_NUMBER)
- `SIGN [DOC]` (e.g., SIGN PAPERWORK)

## VI. NARRATIVE ASSETS (STRING DATABASE)

Use these exact strings for game output to maintain the "Industrial" tone.

- **LOC_HOME_BASE:**
  "LOCATION: HOME BASE (MURFREESBORO).
  TIME: MONDAY, 20:00.
  STATUS: You are at your desk. The gear is piled on the floor.
  OBJECTIVE: Verify the 'Tech Deck' before you sleep. If the drivers fail tomorrow, you don't get paid."

- **LOC_PARKING_LOT:**
  "LOCATION: SITE 404 - SODDY-DAISY, TN.
  TIME: 08:40 EST.
  STATUS: You are sitting in your rental car. The engine is ticking cool. Outside, the warehouse is a grey monolith against a grey sky.
  OBJECTIVE: Establish comms with The Bridge before 08:45."

- **MSG_DRIVER_SUCCESS:**
  "SYSTEM CHECK...
  [OK] USB-to-Serial Controller detected on COM3.
  [OK] Baud Rate: 9600.
  READY FOR CONNECTION."

- **MSG_DRIVER_FAIL:**
  "SYSTEM CHECK...
  [ERROR] DEVICE NOT RECOGNIZED.
  [FATAL] You cannot interface with the client hardware.
  MISSION FAILED: The Client has noticed your delay."

- **MSG_HOTSPOT_CONNECT:**
  "DEPLOYING HOTSPOT...
  SIGNAL: LTE (2 Bars).
  VPN TUNNEL: ESTABLISHED.
  You are now on the corporate network."

- **NPC_BRIDGE_INTRO:**
  "BRIDGE: 'Tech, this is Dispatch. Do I have you on the line? We are on a hard start. Confirm when you are inside the facility.'"



