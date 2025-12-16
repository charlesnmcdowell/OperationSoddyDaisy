import pyfiglet

def get_title_art():
    return pyfiglet.figlet_format("SMART HANDS", font="slant")

def get_game_over_art():
    # Attempting to represent "Sad/Homeless" via text vibe
    art = pyfiglet.figlet_format("BANKRUPT", font="doom")
    art += "\n" + r"""
       .    .
      / \  / \
     (  o  o  )   "Spare some change?"
      \  __  /    (You are fired.)
       \____/
    """
    return art

def get_victory_art():
    # Professional vibe
    art = pyfiglet.figlet_format("SUCCESS", font="doom")
    art += "\n" + r"""
      _______
     /      /,
    /      //
   /______//
  (______(/    "Another job well done."
               (Account Credited)
    """
    return art
