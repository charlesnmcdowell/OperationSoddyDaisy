import sys
import os
import random
from game.state import GameState
import game.assets as assets
import game.art as art

class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.is_running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start(self):
        """Main game loop."""
        self.clear_screen()
        print(art.get_title_art())
        print("Welcome to Smart Hands (v2.1).\n")
        input("Press Enter to Begin...")
        
        while self.is_running:
            self.clear_screen()
            self.display_current_state()
            try:
                user_input = input("\nSelect Option: ")
                if not user_input.isdigit():
                    continue
                self.process_input(user_input)
            except KeyboardInterrupt:
                self.quit_game()

    def display_current_state(self):
        print("-" * 60)
        # Display Bank Balance if relevant (Level 2+)
        if self.state.player_credits > 0:
            print(f"ACCOUNT BALANCE: ${self.state.player_credits:.2f}")
            print("-" * 60)

        if self.state.location == "HOME_BASE":
            print(assets.LOC_HOME_BASE)
            print("\nOPTIONS:")
            print("1. [ACTION] Check Laptop Drivers")
            print("2. [ACTION] Pack All Gear")
            print("3. [TRAVEL] Go to Sleep / Depart for Site")
            
        elif self.state.location == "PARKING_LOT":
            print(assets.LOC_PARKING_LOT)
            print("\nOPTIONS:")
            print("1. [ACTION] Join Bridge Call")
            print("2. [ACTION] Check Inventory")
            print("3. [TRAVEL] Enter Building")
            
        elif self.state.location == "SERVER_ROOM":
            print(assets.LOC_SERVER_ROOM)
            print("\nOPTIONS:")
            print("1. [ACTION] Scan Rack")
            print("2. [ACTION] De-Install Legacy Hardware")
            print("3. [ACTION] Rack & Stack New Gear")
            print("4. [ACTION] Connect Console (The Moment of Truth)")
            
        elif self.state.location == "LOGISTICS":
            print(assets.LOC_LOGISTICS)
            print("\nOPTIONS:")
            print("1. [ACTION] Log Serial Numbers")
            print("2. [ACTION] Ship Gear via FedEx")
            print("3. [FINISH] Close Ticket")
            
        elif self.state.location == "THE_HUB":
            print(assets.LOC_HUB)
            print("\nOPTIONS:")
            print(f"1. [SHOP] Buy Micro-Screwdriver Set ($15.00) {'(OWNED)' if self.state.has_micro_driver else ''}")
            print("2. [JOB] Read Level 2 Brief (Dell-Versa)")
            print("3. [ACCEPT] Deploy to Level 2")

        elif self.state.location == "LEVEL2_SITE":
            print(assets.LOC_LEVEL2_SITE)
            print("\nOPTIONS:")
            print("1. [ACTION] Connect Laptop to Office Wi-Fi")
            print("2. [ACTION] Boot Laptop + Connect Mobile Hotspot")
            print("3. [ACTION] Unplug Old Router Immediately")

        elif self.state.location == "LEVEL2_SWAP":
            print(assets.LOC_LEVEL2_SWAP)
            print("\nOPTIONS:")
            print("1. [ACTION] Use Standard Phillips Driver")
            print("2. [ACTION] Use Micro Phillips (Jeweler's Set)")

        elif self.state.location == "LEVEL2_NEGOTIATION":
            print(assets.LOC_LEVEL2_NEGOTIATION)
            print("\nOPTIONS:")
            print("1. [ACTION] Stay Silent & Finish")
            print("2. [NEGOTIATION] Request +1 Hour Overtime")

    def process_input(self, selection: str):
        selection = selection.strip()
        
        if self.state.location == "HOME_BASE":
            self.handle_home_base(selection)
        elif self.state.location == "PARKING_LOT":
            self.handle_parking_lot(selection)
        elif self.state.location == "SERVER_ROOM":
            self.handle_server_room(selection)
        elif self.state.location == "LOGISTICS":
            self.handle_logistics(selection)
        elif self.state.location == "THE_HUB":
            self.handle_hub(selection)
        elif self.state.location == "LEVEL2_SITE":
            self.handle_level2_site(selection)
        elif self.state.location == "LEVEL2_SWAP":
            self.handle_level2_swap(selection)
        elif self.state.location == "LEVEL2_NEGOTIATION":
            self.handle_level2_negotiation(selection)
        
        if self.is_running:
            input("\nPress Enter to continue...")

    def handle_home_base(self, selection: str):
        if selection == "1":
            self.state.drivers_verified = True
            print("[SYSTEM] USB-to-Serial Controller Active on COM3.")
        elif selection == "2":
            self.state.inventory_packed = True
            self.state.inventory = list(self.state.base_storage)
            print("[SYSTEM] Laptop, Console Cable, and Tools secured.")
        elif selection == "3":
            if not self.state.inventory_packed:
                print("[BLOCK] You cannot leave without your tools.")
            else:
                self.state.location = "PARKING_LOT"

    def handle_parking_lot(self, selection: str):
        if selection == "1":
            self.state.bridge_called = True
            print("[BRIDGE] 'Dispatch here. We have you checked in. You are green to enter.'")
        elif selection == "2":
            print("INVENTORY:")
            print(", ".join(self.state.inventory))
        elif selection == "3":
            if not self.state.bridge_called:
                print("MISSION FAILED. You walked on site without checking in. The client cancelled the ticket.")
                self.quit_game(pause=True)
            else:
                self.state.location = "SERVER_ROOM"

    def handle_server_room(self, selection: str):
        if selection == "1":
            print("It is a 2-Post Relay Rack. The cabling is a mess.")
        elif selection == "2":
            print("Old device removed.")
            self.state.rack_cleared = True
        elif selection == "3":
            print("New hardware mounted. Power connected.")
            self.state.new_gear_installed = True
        elif selection == "4":
            if self.state.drivers_verified:
                print("Console Connected. Configuring Switch...")
                self.state.location = "LOGISTICS"
            else:
                print("CRITICAL FAILURE. Your laptop does not recognize the console cable.") 
                print("You forgot to check the drivers at home. You are fired.")
                self.quit_game(pause=True)

    def handle_logistics(self, selection: str):
        if selection == "1":
            self.state.serials_logged = True
            print("Serial numbers recorded in spreadsheet.")
        elif selection == "2":
            print("Package dropped off. Tracking number saved.")
        elif selection == "3":
            if not self.state.serials_logged:
                print("MISSION FAILED. You shipped the old gear without recording the serials.") 
                print("The client is refusing to pay.")
                self.quit_game(pause=True)
            else:
                print("MISSION COMPLETE. Good work, Deliverator.")
                # Payout Level 1
                payout = 585.00
                print(f"Payment approved. Transferring ${payout:.2f} to account.")
                self.state.player_credits += payout
                self.state.location = "THE_HUB"

    def handle_hub(self, selection: str):
        if selection == "1":
            cost = 15.00
            if self.state.has_micro_driver:
                print("You already own this.")
            elif self.state.player_credits >= cost:
                self.state.player_credits -= cost
                self.state.has_micro_driver = True
                print(f"Purchased Micro-Screwdriver Set. Remaining Balance: ${self.state.player_credits:.2f}")
            else:
                print("Insufficient funds.")
        elif selection == "2":
            print(assets.MSG_L2_BRIEF)
        elif selection == "3":
            if not self.state.has_micro_driver:
                print("[WARNING] You are accepting a job without the required tools. Risk is high.")
            self.state.location = "LEVEL2_SITE"

    def handle_level2_site(self, selection: str):
        if selection == "1":
            print("Connection Failed. The router you are here to replace is broken. You have no internet.")
        elif selection == "2":
            self.state.zoom_active = True
            print("Hotspot 5G Locked. Zoom Bridge Established. WSI Support is online.")
            # Transition immediately or after user input? GDD implies separate actions but menu structure
            # suggests staying on site menu until "proceed" or just transition?
            # GDD says "[CONTINUE] Proceed to Swap" which implies a new menu item or automatic.
            # I'll auto-transition for flow, or add a continue option? 
            # The prompt GDD has [CONTINUE] but I didn't add it to display.
            # Let's simplify: Selecting 2 enables the transition.
            print(assets.MSG_ZOOM_SUCCESS)
            self.state.location = "LEVEL2_SWAP"
        elif selection == "3":
            print("FAILURE. You unplugged the device before the bridge was up.")
            print("WSI Support has no eyes on the site. You are sent home.")
            self.quit_game(pause=True)

    def handle_level2_swap(self, selection: str):
        if selection == "1":
            print("The screws are too small. Your standard driver is stripping the head.")
            print(assets.MSG_TOOL_FAIL)
            self.quit_game(pause=True)
        elif selection == "2":
            if self.state.has_micro_driver:
                print("Smooth turn. Chassis open. Module swapped.")
                self.state.location = "LEVEL2_NEGOTIATION"
            else:
                print("You don't have the Micro Phillips driver!")

    def handle_level2_negotiation(self, selection: str):
        base_pay = 160.00
        overtime = 50.00
        total = base_pay
        
        if selection == "1":
            print("Job ends. Client satisfied.")
        elif selection == "2":
            print("Requesting Overtime...")
            if random.random() > 0.5: # 50/50 Chance
                print("Buyer Approved. Overtime authorized.")
                total += overtime
            else:
                print("Buyer Denied. 'Stick to the cap.'")
        
        self.state.player_credits += total
        print(f"INVOICE SUBMITTED. TOTAL: ${total:.2f}")
        print(f"NEW ACCOUNT BALANCE: ${self.state.player_credits:.2f}")
        
        # End of Content
        print(art.get_victory_art())
        print("LEVEL 2 COMPLETE. Thanks for playing the Career Update!")
        self.quit_game(pause=True)

    def quit_game(self, pause=False):
        if pause:
            input("\nPress Enter to continue...")
        self.clear_screen()
        
        # Check logic for art - if credits > 0 likely not bankrupt/homeless
        if self.state.player_credits > 0 and self.state.location == "LEVEL2_NEGOTIATION":
             # Already printed victory art in negotiation handler
             pass 
        else:
             # Default to game over art if we are quitting abruptly
             print(art.get_game_over_art())

        print("\nGAME OVER.")
        choice = input("Play Again? (Y/N): ").strip().upper()
        if choice == "Y":
            self.state = GameState()
            self.start()
        else:
            print("Exiting...")
            self.is_running = False
            sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.start()
