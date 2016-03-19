# THIRD PARTY
from choices import Choices

CONSTITUENCIES = Choices((
    # TODO: add the other 648 consituencies into here!
    ("Bristol West", "Bristol West"),
    ("Whitney", "Whitney"),

))

PARTIES = Choices((
    # In *alphabetical* order!
    # Names are as per http://www.parliament.uk/mps-lords-and-offices/mps/current-state-of-the-parties/
    ("Conservative", "Conservative"),
    ("Democratic Unionist Party", "Democratic Unionist Party"),
    ("Green", "Green"),
    ("Independent", "Independent"),
    ("Labour", "Labour"),
    ("Liberal Democrat", "Liberal Democrat"),
    ("Plaid Cymru", "Plaid Cymru"),
    ("Scotish National Party", "Scotish National Party"),
    ("Sinn Fein", "Sinn Fein"),
    ("Social Democratic & Labour Party", "Social Democratic & Labour Party"),
    ("Speaker", "Speaker"),
    ("UK Independence", "UK Independence"),
    ("Ulster Unionist Party", "Ulster Unionist Party"),
))
