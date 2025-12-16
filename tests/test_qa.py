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
        # Suppress stdout during tests to keep output clean, unless we want to assert on it
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_scenario_a_happy_path(self):
        """Test Scenario A: The Happy Path (Victory)"""
        game = self.game
        
        # Override quit_game to prevent sys.exit killing the test
        game.quit_game = lambda: setattr(game, 'is_running', False)

        # Phase 0: Home Base
        game.process_input("1") # Check Drivers
        self.assertTrue(game.state.drivers_verified, "Drivers should be verified")
        
        game.process_input("2") # Pack Gear
        self.assertTrue(game.state.inventory_full, "Inventory should be full")
        
        game.process_input("3") # Depart
        self.assertEqual(game.state.location, "PARKING_LOT", "Should be at Parking Lot")

        # Phase 1: Parking Lot
        game.process_input("1") # Bridge Call
        self.assertTrue(game.state.bridge_comms, "Bridge comms should be established")
        
        game.process_input("3") # Enter Building
        self.assertEqual(game.state.location, "SERVER_ROOM", "Should be at Server Room")

        # Phase 2: Server Room
        game.process_input("2") # De-install
        self.assertEqual(game.state.rack_status, "EMPTY", "Rack should be empty")
        self.assertIn("LEGACY_SWITCH", game.state.inventory, "Should have legacy switch")
        
        game.process_input("3") # Rack New
        self.assertEqual(game.state.rack_status, "NEW", "Rack should have new gear")
        
        game.process_input("4") # Connect Console
        self.assertTrue(game.state.switch_configured, "Switch should be configured")
        self.assertEqual(game.state.location, "LOGISTICS", "Should be at Logistics")

        # Phase 3: Logistics
        game.process_input("1") # Log Serial
        self.assertTrue(game.state.serials_logged, "Serials should be logged")
        
        game.process_input("2") # Ship
        self.assertTrue(game.state.legacy_shipped, "Gear should be shipped")
        
        game.process_input("3") # Sign
        self.assertTrue(game.state.paperwork_signed, "Paperwork should be signed")
        
        # 4. Depart (Victory)
        game.process_input("4")
        self.assertFalse(game.is_running, "Game should have ended (Victory)")
        
        # Verify victory message in output
        output = self.held_output.getvalue()
        self.assertIn("MISSION COMPLETE", output)

    def test_scenario_b_lazy_tech_trap(self):
        """Test Scenario B: The 'Lazy Tech' Trap (Game Over)"""
        game = self.game
        game.quit_game = lambda: setattr(game, 'is_running', False)

        # Home Base: Skip Drivers (1)
        game.process_input("2") # Pack
        game.process_input("3") # Depart
        
        self.assertTrue(game.state.driver_failure, "Trap flag should be set")
        self.assertEqual(game.state.location, "PARKING_LOT")

        # Parking Lot: Normal
        game.process_input("1") # Bridge Call
        game.process_input("3") # Enter
        
        # Server Room: Reveal
        game.process_input("4") # Try to connect console
        
        self.assertFalse(game.is_running, "Game should have ended (Failure)")
        output = self.held_output.getvalue()
        self.assertIn("Driver not found", output)

    def test_scenario_c_rogue_entry(self):
        """Test Scenario C: The 'Rogue Entry' (Game Over)"""
        game = self.game
        game.quit_game = lambda: setattr(game, 'is_running', False)

        # Home Base: Normal
        game.process_input("1")
        game.process_input("2")
        game.process_input("3")
        
        # Parking Lot: Skip Bridge Call (1)
        game.process_input("3") # Enter Building
        
        self.assertFalse(game.is_running, "Game should have ended (Failure)")
        output = self.held_output.getvalue()
        self.assertIn("Mission Failed", output)

if __name__ == '__main__':
    unittest.main()

