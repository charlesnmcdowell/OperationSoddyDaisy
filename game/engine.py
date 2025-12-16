import sys
import os
from game.state import GameState
import game.assets as assets
import game.art as art

class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.is_running = True

    def start(self):
        """Main game loop."""
        print(art.get_title_art())
        print("Welcome to Smart Hands.\n")
        
        while self.is_running:
            self.display_current_state()
            try:
                user_input = input("\nSelect Option: ")
                self.process_input(user_input)
            except KeyboardInterrupt:
                self.quit_game()

    def display_current_state(self):
        print("-" * 50)
        if self.state.location == "HOME_BASE":
            print("LOCATION: HOME BASE (MURFREESBORO). TIME: MONDAY, 20:00.")
            print("Objective: Verify your Tech Deck.")
            print("\nOPTIONS:")
            print("1. [ACTION] Check Laptop Drivers")
            print("2. [ACTION] Pack All Gear")
            print("3. [TRAVEL] Go to Sleep / Depart for Site")
            
        elif self.state.location == "PARKING_LOT":
            print("LOCATION: SITE 404 (PARKING LOT). TIME: 08:40.")
            print("Status: You are in the rental car.")
            print("\nOPTIONS:")
            print("1. [ACTION] Join Bridge Call")
            print("2. [ACTION] Check Inventory")
            print("3. [TRAVEL] Enter Building")
            
        elif self.state.location == "SERVER_ROOM":
            print("LOCATION: MDF ROOM. Loud fans. Tangled cables.")
            print("\nOPTIONS:")
            print("1. [ACTION] Scan Rack")
            print("2. [ACTION] De-Install Legacy Hardware")
            print("3. [ACTION] Rack & Stack New Gear")
            print("4. [ACTION] Connect Console")
            
        elif self.state.location == "LOGISTICS":
            print("LOCATION: SITE CLOSEOUT.")
            print("Job done. Cleanup time.")
            print("\nOPTIONS:")
            print("1. [ACTION] Log Serial Numbers")
            print("2. [ACTION] Ship Gear via FedEx")
            print("3. [ACTION] Get Client Signature")
            print("4. [FINISH] Depart Site")

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

    def handle_home_base(self, selection: str):
        if selection == "1":
            print("\n> Checking drivers...")
            print(assets.MSG_DRIVER_SUCCESS)
            self.state.drivers_verified = True
            print("Drivers VERIFIED.")
        elif selection == "2":
            print("\n> Packing gear...")
            self.state.inventory = list(self.state.base_storage)
            self.state.inventory_full = True
            print("All gear packed.")
        elif selection == "3":
            if not self.state.inventory_full:
                print("\n[BLOCK] You cannot leave without your tools! Pack your gear first.")
            else:
                if not self.state.drivers_verified:
                    # THE TRAP
                    self.state.driver_failure = True
                print("\n> You sleep poorly. The next morning, you drive to the site.")
                self.state.location = "PARKING_LOT"
        else:
            print("\nInvalid Selection.")

    def handle_parking_lot(self, selection: str):
        if selection == "1":
            print("\n> Dialing into the bridge...")
            print(assets.NPC_BRIDGE_INTRO)
            self.state.bridge_comms = True
            print("Comms ESTABLISHED.")
        elif selection == "2":
            print("\n> Checking Inventory:")
            print(", ".join(self.state.inventory))
        elif selection == "3":
            if not self.state.bridge_comms:
                print("\n[GAME OVER] You walked in without calling the Bridge. They are angry. Mission Failed.")
                self.quit_game()
            else:
                print("\n> You enter the facility and locate the MDF.")
                self.state.location = "SERVER_ROOM"
        else:
            print("\nInvalid Selection.")

    def handle_server_room(self, selection: str):
        if selection == "1":
            if self.state.rack_status == "LEGACY":
                print("\nRACK 1: Full of dusty legacy gear.")
            elif self.state.rack_status == "EMPTY":
                print("\nRACK 1: Empty rails.")
            elif self.state.rack_status == "NEW":
                print("\nRACK 1: New switch installed.")
                
        elif selection == "2":
            if self.state.rack_status == "LEGACY":
                print("\n> Drilling out old screws...")
                print("Legacy Switch Removed.")
                self.state.rack_status = "EMPTY"
                self.state.add_item("LEGACY_SWITCH")
            else:
                print("\nNothing to de-install.")
                
        elif selection == "3":
            if self.state.rack_status == "EMPTY":
                print("\n> Mounting new gear...")
                print("Click. Snap. The new switch is racked.")
                self.state.rack_status = "NEW"
            elif self.state.rack_status == "LEGACY":
                print("\nRack is full!")
            else:
                print("\nAlready done.")
                
        elif selection == "4":
            print("\n> Connecting Console Cable...")
            # THE REVEAL
            if self.state.driver_failure or not self.state.drivers_verified:
                print(assets.MSG_DRIVER_FAIL)
                print("\n[GAME OVER] Error: Driver not found. You are stuck on site with no way to work. You are fired.")
                self.quit_game()
            else:
                print(assets.MSG_CONSOLE_CONNECT)
                print("Switch Configured. Status: GREEN.")
                self.state.switch_configured = True
                print("\n> The hard part is done. Time for cleanup.")
                self.state.location = "LOGISTICS"
        else:
            print("\nInvalid Selection.")

    def handle_logistics(self, selection: str):
        if selection == "1":
            print("\n> Logging serial numbers...")
            if "LEGACY_SWITCH" in self.state.inventory:
                self.state.serials_logged = True
                print("Legacy Serial: LEGACY_01 recorded.")
            else:
                print("You don't have the old switch to log!")
                
        elif selection == "2":
            if self.state.serials_logged:
                print("\n> Dropping off at FedEx...")
                self.state.legacy_shipped = True
                print("Package Shipped.")
            else:
                print("\n[WARNING] You must log serials before shipping!")
                
        elif selection == "3":
            print("\n> Chasing down the site contact...")
            print("Paperwork SIGNED.")
            self.state.paperwork_signed = True
            
        elif selection == "4":
            # Victory Check
            if self.state.legacy_shipped and self.state.paperwork_signed and self.state.switch_configured:
                print(art.get_victory_art())
                print(assets.MSG_MISSION_SUCCESS)
                self.quit_game()
            else:
                print("\n[BLOCK] You are not done yet!")
                if not self.state.legacy_shipped: print("- Old gear not shipped")
                if not self.state.paperwork_signed: print("- Paperwork not signed")
        else:
            print("\nInvalid Selection.")

    def quit_game(self):
        print(art.get_game_over_art())
        print("Exiting...")
        self.is_running = False
        sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.start()

