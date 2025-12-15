from typing import Tuple, Optional

class Parser:
    def parse_command(self, user_input: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parses raw user input into a (VERB, NOUN) tuple.
        Returns (None, None) if input is empty.
        """
        tokens = user_input.strip().upper().split()
        
        if not tokens:
            return None, None
            
        verb = tokens[0]
        noun = " ".join(tokens[1:]) if len(tokens) > 1 else None
        
        return verb, noun

def normalize_noun(noun: str) -> str:
    """
    Helper to normalize noun strings (e.g. handle synonyms if needed).
    For now, just returns the noun as is.
    """
    if not noun:
        return ""
    return noun



