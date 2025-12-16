from dataclasses import dataclass, field
from typing import List

@dataclass
class GameState:
    location: str = "HOME_BASE"
    inventory: List[str] = field(default_factory=list)
    
    # Global Flags (v2.0)
    inventory_packed: bool = False
    drivers_verified: bool = False
    bridge_called: bool = False
    serials_logged: bool = False
    
    # Phase 2 Helper State
    rack_cleared: bool = False
    new_gear_installed: bool = False

    # Level 2 / Economy State (v2.1)
    player_credits: float = 0.00
    has_micro_driver: bool = False
    zoom_active: bool = False
    
    # Loadout items available at base
    base_storage: List[str] = field(default_factory=lambda: [
        "LAPTOP", "CONSOLE_CABLE", "HOTSPOT", 
        "MONITOR", "DRILL", "CAGE_NUTS", "CAT6_CABLE_X5",
        "VEST", "BOOTS", "HARD_HAT"
    ])
