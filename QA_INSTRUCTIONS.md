# Quality Assurance (QA) Instructions - Smart Hands (v2 Menu System)

**Current Branch:** `dev`
**Objective:** Verify the new menu-driven interface and logic traps.

## How to Run
1. Open Terminal.
2. Navigate to project folder: `cd Documents\OperationSoddyDaisy`
3. Run the game: `.\play.bat`

## Test Scenario A: The Happy Path (Victory)
Follow these exact steps to verify the "Win" state.

**Phase 0: Home Base**
1. Select **1** (Check Laptop Drivers). *Confirm: "Drivers VERIFIED"*
2. Select **2** (Pack All Gear). *Confirm: "All gear packed"*
3. Select **3** (Depart).

**Phase 1: Parking Lot**
1. Select **1** (Join Bridge Call). *Confirm: "Comms ESTABLISHED"*
2. Select **3** (Enter Building).

**Phase 2: Server Room**
1. Select **2** (De-Install Legacy Hardware). *Confirm: "Legacy Switch Removed"*
2. Select **3** (Rack & Stack New Gear). *Confirm: "The new switch is racked"*
3. Select **4** (Connect Console). *Confirm: "Switch Configured. Status: GREEN"*

**Phase 3: Logistics**
1. Select **1** (Log Serial Numbers). *Confirm: "Legacy Serial... recorded"*
2. Select **2** (Ship Gear). *Confirm: "Package Shipped"*
3. Select **3** (Get Client Signature). *Confirm: "Paperwork SIGNED"*
4. Select **4** (Depart Site).
   * **EXPECTED RESULT:** Victory Screen (ASCII Art: SUCCESS).

---

## Test Scenario B: The "Lazy Tech" Trap (Game Over)
Verify that skipping driver checks causes failure later.

1. **Home Base:** Select **2** (Pack), then **3** (Depart). *Skip Option 1!*
2. **Parking Lot:** Select **1** (Call Bridge), then **3** (Enter).
3. **Server Room:** Select **4** (Connect Console).
   * **EXPECTED RESULT:** Game Over Screen. "Error: Driver not found... You are fired."

## Test Scenario C: The "Rogue Entry" (Game Over)
Verify that entering without bridge comms fails immediately.

1. **Home Base:** Do the happy path (1, 2, 3).
2. **Parking Lot:** Select **3** (Enter Building) *without* calling the bridge first.
   * **EXPECTED RESULT:** Game Over Screen. "You walked in without calling the Bridge."

