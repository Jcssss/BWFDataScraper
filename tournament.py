import math

# Represents a Tournament during the badminton season
class Tournament:
    def __init__(self, name, sdate, edate):
        self.name = name # name of tournament
        self.sdate = sdate # start date of tournament
        self.edate = edate # end date of tournament
        self.matches = [] # matches played in the tournament

# Represents the result of a badminton tournament for an event
class Result:
    def __init__(self, event, first, second, third, fourth, third_fourth_diff = False):
        self.event = event # the event, one of MS, XD, WS, MD, WD
        self.first = first # name of first place
        self.second = second # name of second place
        self.third = third # name of third place
        self.fourth = fourth # name of fourth place
        self.third_fourth_diff = third_fourth_diff # was there a match for 3rd place?

# Represents a Match in badminton consisting of two or three games
class Match:
    def __init__(self, winner, event, round, pone, ptwo):
        self.winner = winner # 1 or 2
        self.event = event # the event, one of MS, XD, WS, MD, WD
        self.round = round # the round of the match, a power of 2 or pool
        self.pone = pone # name of player one
        self.ptwo = ptwo # name of player two
        self.games = [] # games played in the match

# Represents a Game in a badminton match
class Game:
    def __init__(self, winner, pone_score, ptwo_score):
        self.winner = winner # 1 or 2
        self.pone_score = pone_score # score of player one
        self.ptwo_score = ptwo_score # score of player two

# Represents a badminton Player
class Player:
    def __init__(self, name, country):
        self.name = name # name of the player
        self.country = country # country the player plays for
