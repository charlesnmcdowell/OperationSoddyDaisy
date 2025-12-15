import sys
from game.state import GameState
from game.parser import Parser
import game.assets as assets
import game.art as art

class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.parser = Parser()
        self.is_running = True

    def start(self):
        """Main game loop."""
        print(art.get_title_art())
        print("Welcome to Smart Hands. Type 'HELP' for commands.\n")
        self.print_location_intro()
        
        while self.is_running:
            try:
                user_input = input("\n> ")
                self.process_input(user_input)
            except KeyboardInterrupt:
                self.quit_game()

    def print_location_intro(self):
        if self.state.location == "HOME_BASE":
            print(assets.LOC_HOME_BASE)
        elif self.state.location == "PARKING_LOT":
            print(assets.LOC_PARKING_LOT)
        elif self.state.location == "SITE_ENTRANCE":
            print(assets.LOC_SITE_ENTRANCE)
        elif self.state.location == "SERVER_ROOM":
            print(assets.LOC_SERVER_ROOM)
        elif self.state.location == "FEDEX":
            print(assets.LOC_FEDEX)
            
    def process_input(self, user_input: str):
        verb, noun = self.parser.parse_command(user_input)
        
        if not verb:
            return

        if verb == "QUIT" or verb == "EXIT":
            self.quit_game()
        elif verb == "SCAN":
            self.handle_scan(noun)
        elif verb == "CHECK":
            self.handle_check(noun)
        elif verb == "LIST":
            self.handle_list(noun)
        elif verb == "DEPLOY":
            self.handle_deploy(noun)
        elif verb == "CONNECT" or verb == "CALL":
            self.handle_connect(noun)
        elif verb == "MOVE":
            self.handle_move(noun)
        elif verb == "TAKE":
            self.handle_take(noun)
        elif verb == "LOG":
            self.handle_log(noun)
        elif verb == "TYPE":
            self.handle_type(noun)
        elif verb == "SHIP":
            self.handle_ship(noun)
        elif verb == "SIGN":
            self.handle_sign(noun)
        elif verb == "UPLOAD":
            self.handle_upload(noun)
        elif verb == "HELP":
            self.print_help()
        else:
            print("Unknown command.")

    def print_help(self):
        print("COMMANDS:")
        print("  SCAN [TARGET]       - Look at something")
        print("  CHECK [STATUS]      - Check status (TIME, DRIVER, SIGNAL)")
        print("  LIST INVENTORY      - Show your gear")
        print("  DEPLOY [ITEM]       - Use an item")
        print("  CONNECT [TARGET]    - Connect to bridge or console")
        print("  MOVE [LOCATION]     - Travel")
        print("  TAKE [ITEM]         - Pick up item")
        print("  LOG [SERIAL]        - Record serial number")
        print("  TYPE [CMD]          - Type into console")
        print("  SHIP [ITEM]         - Ship package")
        print("  SIGN [DOC]          - Sign paperwork")
        print("  UPLOAD [DOCS]       - Upload documentation")
        print("  QUIT                - Exit game")

    def handle_take(self, noun: str):
        if self.state.location == "HOME_BASE":
            if noun in self.state.base_storage:
                self.state.add_item(noun)
                self.state.base_storage.remove(noun)
                print(f"You took the {noun}.")
            elif noun == "ALL":
                # specific override for quality of life
                for item in list(self.state.base_storage):
                    if item not in self.state.inventory:
                        self.state.add_item(item)
                        self.state.base_storage.remove(item)
                print("You took all the gear.")
            else:
                print(f"Cannot take {noun}.")
        elif self.state.location == "SERVER_ROOM":
            if noun == "LEGACY_SWITCH":
                if self.state.rack_status == "EMPTY": # Means we drilled it out
                    if "LEGACY_SWITCH" not in self.state.inventory:
                        self.state.add_item("LEGACY_SWITCH")
                        print("You pick up the heavy legacy switch.")
                    else:
                        print("You already have it.")
                elif self.state.rack_status == "LEGACY":
                    print("It's still screwed into the rack. Use a DRILL.")
                else:
                    print("There is no legacy switch here.")
            else:
                print("You can't take that.")
        else:
             print("You can't take that here.")

    def handle_scan(self, noun: str):
        if self.state.location == "HOME_BASE":
            if noun == "ROOM" or noun is None:
                if self.state.base_storage:
                    print("You see your gear piled on the floor: " + ", ".join(self.state.base_storage))
                else:
                    print("The floor is empty. You have packed everything.")
            elif noun in self.state.base_storage:
                print(f"Standard issue {noun}.")
        elif self.state.location == "PARKING_LOT":
            if noun == "ROOM" or noun is None:
                print("You are in the parking lot. The warehouse looms ahead.")
            elif noun == "CAR":
                print("It's a rental. Clean, but soulless.")
        elif self.state.location == "SERVER_ROOM":
            if noun == "RACK" or noun == "ROOM" or noun is None:
                if self.state.rack_status == "LEGACY":
                    print("RACK 1: Contains LEGACY_SWITCH (SN: LEGACY_01). Cables are messy.")
                elif self.state.rack_status == "EMPTY":
                    print("RACK 1: Empty. Ready for new gear.")
                elif self.state.rack_status == "NEW":
                    print("RACK 1: NEW_SWITCH installed. Uplink is dark.")
                
                # Check for new gear on floor
                if self.state.rack_status != "NEW":
                    print("ON FLOOR: A box containing NEW_SWITCH.")
            elif noun == "LEGACY_SWITCH":
                 print("Old rusted hardware. Needs to go.")
        elif self.state.location == "FEDEX":
            print("You are at the FedEx counter.")

    def handle_check(self, noun: str):
        if noun == "DRIVER":
            if "LAPTOP" in self.state.inventory or self.state.location == "HOME_BASE": 
                print(assets.MSG_DRIVER_SUCCESS)
                self.state.set_flag("DRIVERS_VERIFIED")
            else:
                print("You need your laptop to check drivers.")
        elif noun == "TIME":
            print("Time is ticking.")
        elif noun == "SIGNAL" and self.state.location == "PARKING_LOT":
            if self.state.check_flag("VPN_ESTABLISHED"):
                 print("SIGNAL: LTE (2 Bars). VPN: CONNECTED.")
            else:
                 print("SIGNAL: No connection. Deploy Hotspot required.")
        elif noun == "STATUS" or noun == "MISSION":
            self.check_mission_status(verbose=True)

    def handle_list(self, noun: str):
        if noun == "INVENTORY" or noun is None:
            if not self.state.inventory:
                print("Inventory is empty.")
            else:
                print("Inventory: " + ", ".join(self.state.inventory))

    def handle_deploy(self, noun: str):
        if noun == "HOTSPOT":
            if "HOTSPOT" in self.state.inventory:
                print(assets.MSG_HOTSPOT_CONNECT)
                self.state.set_flag("VPN_ESTABLISHED")
            else:
                print("You don't have a hotspot.")
        elif noun == "DRILL":
            if "DRILL" in self.state.inventory:
                if self.state.location == "SERVER_ROOM" and self.state.rack_status == "LEGACY":
                    print("You unscrew the old gear. Dust goes everywhere. LEGACY_SWITCH removed.")
                    self.state.rack_status = "EMPTY"
                else:
                    print("Nothing to drill here.")
            else:
                print("You don't have a drill.")
        elif noun == "NEW_SWITCH":
            if self.state.location == "SERVER_ROOM" and self.state.rack_status == "EMPTY":
                if "CAGE_NUTS" in self.state.inventory:
                    print("You mount the NEW_SWITCH using the cage nuts. It clicks into place.")
                    self.state.rack_status = "NEW"
                else:
                    print("You can't mount it without CAGE_NUTS.")
            elif self.state.rack_status == "LEGACY":
                print("Rack is full. Remove old gear first.")
            else:
                print("Can't deploy that here.")
        else:
            print(f"You can't deploy {noun} right now.")

    def handle_connect(self, noun: str):
        if noun == "BRIDGE" or noun == "DISPATCH":
            if self.state.check_flag("VPN_ESTABLISHED"):
                print(assets.NPC_BRIDGE_INTRO)
                self.state.set_flag("COMMS_ESTABLISHED")
                # Also check mission status if end game
                if self.state.docs_uploaded:
                    self.check_mission_status(verbose=True)
            else:
                print("No connection. You need to get online first.")
        elif noun == "CONSOLE" or noun == "CONSOLE_CABLE" or noun == "CABLE":
            if self.state.location == "SERVER_ROOM":
                if "CONSOLE_CABLE" in self.state.inventory and "LAPTOP" in self.state.inventory:
                    if self.state.check_flag("DRIVERS_VERIFIED"):
                        if self.state.rack_status == "NEW":
                            print(assets.MSG_CONSOLE_CONNECT)
                            self.state.console_connected = True
                        elif self.state.rack_status == "LEGACY":
                             print("Connecting to Legacy Switch...")
                             print(assets.MSG_CONSOLE_CONNECT)
                             self.state.console_connected = True
                        else:
                            print("Nothing to connect to.")
                    else:
                        print(assets.MSG_DRIVER_FAIL)
                else:
                    print("You need a laptop and console cable.")
            else:
                print("Nothing to console into here.")
        else:
            print(f"Cannot connect {noun}.")

    def handle_move(self, noun: str):
        if noun == "TO PARKING_LOT" or noun == "PARKING_LOT":
            if self.state.location == "HOME_BASE":
                criticals = ["LAPTOP", "CONSOLE_CABLE", "HOTSPOT"]
                missing = [item for item in criticals if item not in self.state.inventory]
                self.state.location = "PARKING_LOT"
                self.print_location_intro()
                if missing:
                    print(f"WARNING: You left without: {', '.join(missing)}")
                    print("MISSION FAILED: You arrived at site without critical gear.")
                    self.quit_game()
            elif self.state.location == "SITE_ENTRANCE":
                self.state.location = "PARKING_LOT"
                self.print_location_intro()
            elif self.state.location == "FEDEX":
                self.state.location = "PARKING_LOT"
                self.print_location_intro()
        
        elif noun == "TO SITE" or noun == "SITE" or noun == "WAREHOUSE" or noun == "INSIDE" or noun == "SITE_ENTRANCE":
            if self.state.location == "PARKING_LOT":
                if self.state.check_flag("COMMS_ESTABLISHED"):
                    self.state.location = "SITE_ENTRANCE"
                    self.print_location_intro()
                else:
                    print("You cannot enter until you've established comms with the Bridge.")
            elif self.state.location == "SERVER_ROOM":
                self.state.location = "SITE_ENTRANCE"
                self.print_location_intro()
        
        elif noun == "SERVER_ROOM" or noun == "TO SERVER_ROOM":
            if self.state.location == "SITE_ENTRANCE":
                self.state.location = "SERVER_ROOM"
                self.print_location_intro()
        
        elif noun == "FEDEX" or noun == "TO FEDEX":
            if self.state.location == "PARKING_LOT":
                self.state.location = "FEDEX"
                self.print_location_intro()
            else:
                print("You can't go there from here (Go to Parking Lot first).")

    def handle_log(self, noun: str):
        if self.state.location == "SERVER_ROOM":
            if noun == "LEGACY_01" or noun == "SERIAL_NUMBER" or noun == "LEGACY_SWITCH_SN": 
                if self.state.rack_status == "LEGACY":
                    print("Logged Serial Number: LEGACY_01")
                    self.state.logged_serials.add("LEGACY_01")
                else:
                    print("Cannot log serial number (device missing).")
            else:
                print(f"Logged {noun}.")
                self.state.logged_serials.add(noun)
        else:
            print("Nothing to log here.")

    def handle_type(self, noun: str):
        if self.state.console_connected:
            print(f"SENT: {noun}")
            print("SWITCH: [OK]")
            if noun and ("COPY" in noun or "CONFIG" in noun or "UPLOAD" in noun):
                 print("Configuration uploaded successfully. Switch is GREEN.")
                 self.state.set_flag("SWITCH_CONFIGURED")
        else:
            print("Console not connected.")

    def handle_ship(self, noun: str):
        if self.state.location == "FEDEX":
            if "LEGACY_SWITCH" in self.state.inventory:
                if "LEGACY_01" in self.state.logged_serials:
                    print("You hand over the box. Clerk slaps a label on it.")
                    print("TRACKING NUMBER: 1Z99999999")
                    self.state.legacy_shipped = True
                    self.state.remove_item("LEGACY_SWITCH")
                else:
                    print("ERROR: The Ghost Error. You didn't log the serial number before shipping!")
                    print("MISSION FAILED.")
                    self.quit_game()
            else:
                print("You don't have the package to ship.")
        else:
            print("You are not at FedEx.")

    def handle_sign(self, noun: str):
        if self.state.location == "SITE_ENTRANCE":
            print("You ask the guard for the sign-off.")
            print("Guard: 'Did you finish? Okay, sign here.'")
            print("Paperwork SIGNED.")
            self.state.paperwork_signed = True
        else:
            print("No one to sign paperwork here.")

    def handle_upload(self, noun: str):
        if noun == "DOCS" or noun == "DOCUMENTATION":
            if self.state.check_flag("VPN_ESTABLISHED"):
                print("Uploading photos... Uploading logs... Uploading sign-off...")
                if self.state.legacy_shipped and self.state.paperwork_signed and self.state.check_flag("SWITCH_CONFIGURED"):
                    print("UPLOAD COMPLETE.")
                    self.state.docs_uploaded = True
                    self.check_mission_status(verbose=True)
                else:
                     print("UPLOAD INCOMPLETE. You are missing something.")
                     if not self.state.legacy_shipped: print("- Shipping Manifest")
                     if not self.state.paperwork_signed: print("- Client Signature")
                     if not self.state.check_flag("SWITCH_CONFIGURED"): print("- Switch Configuration")
            else:
                print("No internet connection. Deploy Hotspot?")
        else:
            print(f"Cannot upload {noun}.")

    def check_mission_status(self, verbose=False):
        # Victory Conditions
        # Hardware installed and Green (SWITCH_CONFIGURED)
        # Old gear logged and shipped (legacy_shipped + logged_serials check inside ship)
        # Sign-off sheet (paperwork_signed)
        # Docs uploaded (docs_uploaded)
        
        if (self.state.check_flag("SWITCH_CONFIGURED") and 
            self.state.legacy_shipped and 
            self.state.paperwork_signed and 
            self.state.docs_uploaded):
            
            print(art.get_victory_art())
            print(assets.MSG_MISSION_SUCCESS)
            self.quit_game()
        else:
            if verbose:
                print("Mission Status: INCOMPLETE")
                # Could list missing items here

    def quit_game(self):
        print(art.get_game_over_art())
        print("Exiting...")
        self.is_running = False
        sys.exit()

if __name__ == "__main__":
    game = GameEngine()
    game.start()
