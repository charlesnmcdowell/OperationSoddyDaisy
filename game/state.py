from dataclasses import dataclass, field
from typing import List, Set, Dict

@dataclass
class GameState:
    location: str = "HOME_BASE"
    inventory: List[str] = field(default_factory=list)
    flags: Set[str] = field(default_factory=set)
    mission_phase: int = 0
    
    # Phase 2 State
    logged_serials: Set[str] = field(default_factory=set)
    rack_status: str = "LEGACY" # LEGACY, EMPTY, NEW
    console_connected: bool = False
    
    # Phase 3 & 4 State
    legacy_shipped: bool = False
    paperwork_signed: bool = False
    docs_uploaded: bool = False
    
    # Loadout items available at base
    base_storage: List[str] = field(default_factory=lambda: [
        "LAPTOP", "CONSOLE_CABLE", "HOTSPOT", 
        "MONITOR", "DRILL", "CAGE_NUTS", "CAT6_CABLE_X5",
        "VEST", "BOOTS", "HARD_HAT"
    ])

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def add_item(self, item: str):
        self.inventory.append(item)

    def remove_item(self, item: str):
        if item in self.inventory:
            self.inventory.remove(item)
            
    def set_flag(self, flag: str):
        self.flags.add(flag)
        
    def check_flag(self, flag: str) -> bool:
        return flag in self.flags
