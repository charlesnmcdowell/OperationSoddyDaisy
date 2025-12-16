import sys
import os
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
        print("Welcome to Smart Hands (v2.0).\n")
        input("Press Enter to Begin...")
        
        while self.is_running:
            self.clear_screen()
            self.display_current_state()
            try:
                user_input = input("\nSelect Option: ")
                # Validate input is integer
                if not user_input.isdigit():
                    continue
                self.process_input(user_input)
            except KeyboardInterrupt:
                self.quit_game()

    def display_current_state(self):
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
                # Transition even if drivers not verified (Trap)
                self.state.location = "PARKING_LOT"
        else:
             pass # Invalid input just loops back

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
        else:
            pass

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
                print("You forgot to check the drivers at home.") 
                print("You cannot complete the work. You are fired.")
                self.quit_game(pause=True)
        else:
            pass

    def handle_logistics(self, selection: str):
        if selection == "1":
            self.state.serials_logged = True
            print("Serial numbers recorded in spreadsheet.")
                
        elif selection == "2":
            print("Package dropped off. Tracking number saved.")
            
        elif selection == "3":
            if not self.state.serials_logged:
                print("MISSION FAILED. You shipped the old gear without recording the serials.") 
                print("The equipment is lost. The client is refusing to pay.")
                self.quit_game(pause=True)
            else:
                print("MISSION COMPLETE. Good work, Deliverator. Payment authorized.")
                self.quit_game(pause=True)
        else:
            pass

    def quit_game(self, pause=False):
        if pause:
            input("\nPress Enter to exit...")
        self.clear_screen()
        if self.state.serials_logged and self.state.location == "LOGISTICS":
             print(art.get_victory_art())
        else:
             print(art.get_game_over_art())
        print("Exiting...")
        self.is_running = False
        sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.start()
