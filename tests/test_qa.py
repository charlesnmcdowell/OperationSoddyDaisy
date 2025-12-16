import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

# Add project root to path so we can import game
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.engine import GameEngine

class TestSmartHandsQA(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine()
        # Suppress stdout and screen clearing
        self.game.clear_screen = lambda: None
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_scenario_a_happy_path(self):
        """Test Scenario A: The Happy Path (Victory)"""
        game = self.game
        
        # Override quit_game to prevent sys.exit
        game.quit_game = lambda pause=False: setattr(game, 'is_running', False)

        # Phase 0: Home Base
        game.handle_home_base("1") # Check Drivers
        self.assertTrue(game.state.drivers_verified)
        
        game.handle_home_base("2") # Pack Gear
        self.assertTrue(game.state.inventory_packed)
        
        game.handle_home_base("3") # Depart
        self.assertEqual(game.state.location, "PARKING_LOT")

        # Phase 1: Parking Lot
        game.handle_parking_lot("1") # Bridge Call
        self.assertTrue(game.state.bridge_called)
        
        game.handle_parking_lot("3") # Enter Building
        self.assertEqual(game.state.location, "SERVER_ROOM")

        # Phase 2: Server Room
        game.handle_server_room("2") # De-install
        game.handle_server_room("3") # Rack New
        
        game.handle_server_room("4") # Connect Console
        self.assertEqual(game.state.location, "LOGISTICS")

        # Phase 3: Logistics
        game.handle_logistics("1") # Log Serial
        self.assertTrue(game.state.serials_logged)
        
        game.handle_logistics("2") # Ship
        
        # 3. Finish (Victory)
        game.handle_logistics("3")
        self.assertFalse(game.is_running)
        
        # Verify output contains victory text
        output = self.held_output.getvalue()
        self.assertIn("MISSION COMPLETE", output)

    def test_scenario_b_lazy_tech_trap(self):
        """Test Scenario B: The 'Lazy Tech' Trap (Game Over)"""
        game = self.game
        game.quit_game = lambda pause=False: setattr(game, 'is_running', False)

        # Home Base: Skip Drivers (1)
        game.handle_home_base("2") # Pack
        game.handle_home_base("3") # Depart
        self.assertEqual(game.state.location, "PARKING_LOT")

        # Parking Lot: Normal
        game.handle_parking_lot("1") # Bridge Call
        game.handle_parking_lot("3") # Enter
        
        # Server Room: Reveal
        game.handle_server_room("4") # Try to connect console
        
        self.assertFalse(game.is_running)
        output = self.held_output.getvalue()
        self.assertIn("CRITICAL FAILURE", output)

    def test_scenario_c_rogue_entry(self):
        """Test Scenario C: The 'Rogue Entry' (Game Over)"""
        game = self.game
        game.quit_game = lambda pause=False: setattr(game, 'is_running', False)

        # Home Base: Normal
        game.handle_home_base("1")
        game.handle_home_base("2")
        game.handle_home_base("3")
        
        # Parking Lot: Skip Bridge Call (1)
        game.handle_parking_lot("3") # Enter Building
        
        self.assertFalse(game.is_running)
        output = self.held_output.getvalue()
        self.assertIn("MISSION FAILED", output)

if __name__ == '__main__':
    unittest.main()
