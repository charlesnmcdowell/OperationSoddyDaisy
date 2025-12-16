from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class GameState:
    location: str = "HOME_BASE"
    inventory: List[str] = field(default_factory=list)
    flags: Set[str] = field(default_factory=set)
    mission_phase: int = 0
    
    # New specific flags for Menu Logic
    drivers_verified: bool = False
    driver_failure: bool = False # The "trap" flag
    inventory_full: bool = False
    bridge_comms: bool = False
    serials_logged: bool = False
    legacy_shipped: bool = False
    paperwork_signed: bool = False
    switch_configured: bool = False
    
    # Phase 2 State
    rack_status: str = "LEGACY" # LEGACY, EMPTY, NEW
    console_connected: bool = False
    
    # Loadout items available at base (simplified for menu logic check)
    base_storage: List[str] = field(default_factory=lambda: [
        "LAPTOP", "CONSOLE_CABLE", "HOTSPOT", 
        "MONITOR", "DRILL", "CAGE_NUTS", "CAT6_CABLE_X5",
        "VEST", "BOOTS", "HARD_HAT"
    ])

    def add_item(self, item: str):
        self.inventory.append(item)

    def remove_item(self, item: str):
        if item in self.inventory:
            self.inventory.remove(item)
            
    def set_flag(self, flag: str):
        self.flags.add(flag)
        
    def check_flag(self, flag: str) -> bool:
        return flag in self.flags

