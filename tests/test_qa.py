import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.engine import GameEngine

class TestSmartHandsQA(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine()
        self.game.clear_screen = lambda: None
        self.held_output = StringIO()
        sys.stdout = self.held_output
        self.game.quit_game = lambda pause=False: setattr(self.game, 'is_running', False)

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_career_happy_path(self):
        """Test Full Career Path: Level 1 -> Hub -> Level 2 Victory"""
        game = self.game

        # --- LEVEL 1 ---
        game.handle_home_base("1") # Drivers
        game.handle_home_base("2") # Pack
        game.handle_home_base("3") # Depart
        
        game.handle_parking_lot("1") # Bridge
        game.handle_parking_lot("3") # Enter
        
        game.handle_server_room("4") # Console
        
        game.handle_logistics("1") # Log
        game.handle_logistics("3") # Close Ticket (Triggers Payout)
        
        self.assertEqual(game.state.location, "THE_HUB")
        self.assertEqual(game.state.player_credits, 585.00)

        # --- THE HUB ---
        game.handle_hub("1") # Buy Micro Driver
        self.assertTrue(game.state.has_micro_driver)
        self.assertEqual(game.state.player_credits, 570.00) # 585 - 15
        
        game.handle_hub("3") # Deploy
        self.assertEqual(game.state.location, "LEVEL2_SITE")

        # --- LEVEL 2 ---
        game.handle_level2_site("2") # Boot Laptop + Hotspot
        self.assertTrue(game.state.zoom_active)
        self.assertEqual(game.state.location, "LEVEL2_SWAP")

        game.handle_level2_swap("2") # Use Micro Driver
        self.assertEqual(game.state.location, "LEVEL2_NEGOTIATION")
        
        game.handle_level2_negotiation("1") # Finish (Safe pay)
        
        self.assertGreater(game.state.player_credits, 570.00) # Should have earned at least 160
        self.assertFalse(game.is_running)

    def test_level2_trap_wifi(self):
        """Test Level 2 Trap: Connecting to broken wifi"""
        game = self.game
        game.state.location = "LEVEL2_SITE"
        
        game.handle_level2_site("1")
        output = self.held_output.getvalue()
        self.assertIn("Connection Failed", output)
        # Should NOT advance
        self.assertEqual(game.state.location, "LEVEL2_SITE")

    def test_level2_trap_unplug(self):
        """Test Level 2 Trap: Unplugging early"""
        game = self.game
        game.state.location = "LEVEL2_SITE"
        
        game.handle_level2_site("3")
        self.assertFalse(game.is_running)
        output = self.held_output.getvalue()
        self.assertIn("FAILURE", output)

if __name__ == '__main__':
    unittest.main()
