"""
teamStats.py contains the TeamStats class and the VersusStats class
"""

import numpy as np
from collections import defaultdict

teamStatsDataType = [("Date", "U10"), ("Pass Atts", np.ubyte), ("Completions", np.ubyte), ("First Downs", np.ubyte),
                     ("4th Conv", np.ubyte), ("4th Conv Lost", np.ubyte), ("Fumbles", np.ubyte), ("Fumbles Lost", np.ubyte),
                     ("Interceptions", np.ubyte), ("Location", "U4"), ("Net Pass Yards", np.ushort), ("Outcome", "U1"),
                     ("Pass TDs", np.ubyte), ("Pass Yards", np.ushort), ("Penalties", np.ubyte), ("Penalty Yards", np.ushort),
                     ("Rush Atts", np.ubyte), ("Rush TDs", np.ubyte), ("Rush Yards", np.ushort), ("Sacks", np.ubyte),
                     ("Sack Yards", np.ushort), ("Score", np.ubyte), ("3rd Conv", np.ubyte), ("3rd Conv Lost", np.ubyte),
                     ("Time of Poss", np.ushort), ("Total Yards", np.ushort), ("Turnovers", np.ubyte)]

vsStatsDataType = [("Date", "U10"), ("Opponent", "U3"), ("Pass Atts", np.ubyte), ("Completions", np.ubyte), ("First Downs", np.ubyte),
                    ("4th Conv", np.ubyte), ("4th Conv Lost", np.ubyte), ("Fumbles", np.ubyte), ("Fumbles Lost", np.ubyte),
                    ("Interceptions", np.ubyte), ("Location", "U4"), ("Net Pass Yards", np.ushort), ("Outcome", "U1"),
                    ("Pass TDs", np.ubyte), ("Pass Yards", np.ushort), ("Penalties", np.ubyte), ("Penalty Yards", np.ushort),
                    ("Rush Atts", np.ubyte), ("Rush TDs", np.ubyte), ("Rush Yards", np.ushort), ("Sacks", np.ubyte),
                    ("Sack Yards", np.ushort), ("Score", np.ubyte), ("3rd Conv", np.ubyte), ("3rd Conv Lost", np.ubyte),
                    ("Time of Poss", np.ushort), ("Total Yards", np.ushort), ("Turnovers", np.ubyte)]

class VersusStats():
    # Class containing the statistics for a team against a specific opponent
    def __init__(self, oppName):
        pass

    def updateStats(self, score, oppScore, yards, TO, oppYards, oppTO):
        pass

    def getStats(self):
        pass

class TeamStats():
    # Class containing the statistics for a team
    def __init__(self, nameSymbol):
        self.nameSymbol = nameSymbol                                # Name of the team
        self.performance = np.array([], dtype=teamStatsDataType)    # Array containing the performance data for each game

    def addPerformance(self, game):
        # Add a new performance to the team's stats
        if game[2] == self.nameSymbol:
            performance = np.array(tuple([game[1]] + list(game[3:int(((len(game) - 2) / 2) + 2)])), dtype=teamStatsDataType)
            vsPerformance = np.array(tuple([game[1]] + list(game[0] + game[int(((len(game) - 2) / 2) + 2):])), dtype=teamStatsDataType)
        else:
            performance = np.array(tuple([game[1]] + list(game[int(((len(game) - 2) / 2) + 2):])), dtype=teamStatsDataType)
            vsPerformance = np.array(tuple([game[1]] + list(game[0] + game[3:int(((len(game) - 2) / 2) + 2)])), dtype=teamStatsDataType)
        self.performance = np.append(self.performance, performance)

    def getStats(self):
        pass

    def getStatsVS(self, opponent):
        pass