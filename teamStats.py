"""
teamStats.py contains the TeamStats class and the VersusStats class
"""

import numpy as np
from collections import defaultdict
from teams import teamDict

statsDataType = np.dtype([("Date", "datetime64[D]"), ("Opponent Name Symbol", "U3"), ("Pass Atts", np.ubyte), ("Completions", np.ubyte), ("First Downs", np.ubyte),
                          ("4th Conv", np.ubyte), ("4th Conv Lost", np.ubyte), ("Fumbles", np.ubyte), ("Fumbles Lost", np.ubyte),
                          ("Interceptions", np.ubyte), ("Location", "U4"), ("Net Pass Yards", np.ushort), ("Outcome", "U1"),
                          ("Pass TDs", np.ubyte), ("Pass Yards", np.ushort), ("Penalties", np.ubyte), ("Penalty Yards", np.ushort),
                          ("Rush Atts", np.ubyte), ("Rush TDs", np.ubyte), ("Rush Yards", np.ushort), ("Sacks", np.ubyte),
                          ("Sack Yards", np.ushort), ("Score", np.ubyte), ("3rd Conv", np.ubyte), ("3rd Conv Lost", np.ubyte),
                          ("Time of Poss", np.ushort), ("Total Yards", np.ushort), ("Turnovers", np.ubyte)])

vsStatsDataType = np.dtype([("Date", "datetime64[D]"), ("Pass Atts", np.ubyte), ("Completions", np.ubyte), ("First Downs", np.ubyte),
                            ("4th Conv", np.ubyte), ("4th Conv Lost", np.ubyte), ("Fumbles", np.ubyte), ("Fumbles Lost", np.ubyte),
                            ("Interceptions", np.ubyte), ("Location", "U4"), ("Net Pass Yards", np.ushort), ("Outcome", "U1"),
                            ("Pass TDs", np.ubyte), ("Pass Yards", np.ushort), ("Penalties", np.ubyte), ("Penalty Yards", np.ushort),
                            ("Rush Atts", np.ubyte), ("Rush TDs", np.ubyte), ("Rush Yards", np.ushort), ("Sacks", np.ubyte),
                            ("Sack Yards", np.ushort), ("Score", np.ubyte), ("3rd Conv", np.ubyte), ("3rd Conv Lost", np.ubyte),
                            ("Time of Poss", np.ushort), ("Total Yards", np.ushort), ("Turnovers", np.ubyte)])

class VersusStats():
    # Class containing the statistics for a team against a specific opponent
    def __init__(self, oppNameSymbol):
        self.nameSymbol = oppNameSymbol                         # Name of the opponent
        self.performance = np.array([], dtype=vsStatsDataType)  # Array containing the performance data for each game

    def addPerformance(self, game):
        # Add a new performance to the teams' stats
        performance = np.array(game, dtype=vsStatsDataType)
        self.performance = np.append(self.performance, performance)

    def getStats(self, date):
        # Get the stats for a specific date
        statDict = {}
        games = self.performance
        for stat in vsStatsDataType.names:
            # Generate stat averages
            if stat in ("Date", "Outcome", "Location"):
                continue
            statDict[stat + "OppAvg"] = np.average(games[games["Date"] <= date][stat])

        gamesBeforeDate = games[games["Date"] <= date]
        statDict["winOppAvg"] = len(gamesBeforeDate[gamesBeforeDate["Outcome"] == "W"]) / len(games[games["Date"] <= date])
        statDict["winOpp"] = int(games[games["Date"] == date]["Outcome"] == "W")
        statDict["homeOpp"] = int(games[games["Date"] == date]["Location"] == "Home")

        return statDict


class TeamStats():
    # Class containing the statistics for a team
    def __init__(self, nameSymbol):
        self.nameSymbol = nameSymbol                            # Name of the team
        self.performance = np.array([], dtype=statsDataType)    # Array containing the performance data for each game
        self.vsPerformance = defaultdict(VersusStats)           # Dictionary containing the performance data for each opponent
        self.gamesPlayed = 0                                    # Number of games played

    def addPerformance(self, game):
        # Add a new performance to the teams' stats
        # The indexes are semi-hardcoded, indexes 0 and 1 are the game id and the date
        # The rest of the data can be divided into 2 congruent groups, the team's and the opponent's
        # The first index of each group is the team's name symbol
        self.gamesPlayed += 1

        date = np.datetime64(game[1])
        secondGroupIndex = int(((len(game) - 2) / 2) + 2)
        nameSymbolA = game[2]
        nameSymbolB = game[secondGroupIndex]
        if nameSymbolA == self.nameSymbol:
            oppNameSymbol = nameSymbolB
            performance = np.array(tuple([date, oppNameSymbol] + game[3:secondGroupIndex]), dtype=statsDataType)
            vsPerformance = tuple([date] + game[secondGroupIndex + 1:])
        else:
            oppNameSymbol = nameSymbolA
            performance = np.array(tuple([date, oppNameSymbol] + game[secondGroupIndex + 1:]), dtype=statsDataType)
            vsPerformance = tuple([date] + game[3:secondGroupIndex])

        self.performance = np.append(self.performance, performance)

        if oppNameSymbol not in self.vsPerformance:
            self.vsPerformance[oppNameSymbol] = VersusStats(oppNameSymbol)
        self.vsPerformance[oppNameSymbol].addPerformance(vsPerformance)

    def getStats(self):
        # Return the stats for the team
        stats = []
        games = self.performance
        for date in np.nditer(games["Date"]):
            # TODO: Turn generating averages into a for loop
            statDict = {}
            for stat in statsDataType.names:
                if stat in ("Date", "Opponent Name Symbol", "Outcome", "Location"):
                    continue
                # Generate stat averages
                statDict[stat + "Avg"] = np.average(games[games["Date"] <= date][stat])

            gamesBeforeDate = games[games["Date"] <= date]
            statDict["winAvg"] = len(gamesBeforeDate[gamesBeforeDate["Outcome"] == "W"]) / len(games[games["Date"] <= date])
            statDict["win"] = int(games[games["Date"] == date]["Outcome"] == "W")
            statDict["home"] = int(games[games["Date"] == date]["Location"] == "Home")

            oppNameSymbol = games[games["Date"] == date]["Opponent Name Symbol"].item()
            statDict.update(self.vsPerformance[oppNameSymbol].getStats(date))

            stats.append(statDict)

        return stats

    def printGames(self):
        for game in np.nditer(self.performance):
            print(game)

class statCEO():
    # Executive class for team stats
    def __init__(self):
        self.teams = defaultdict(TeamStats)    # Dictionary containing the team stats for each team

    def addPerformance(self, game):
        # Add a new performance to the teams' stats
        nameSymbolA = game[2]
        if nameSymbolA not in self.teams:
            self.teams[nameSymbolA] = TeamStats(nameSymbolA)
        self.teams[nameSymbolA].addPerformance(game)

        nameSymbolB = game[int(((len(game) - 2) / 2) + 3)]
        if nameSymbolB not in self.teams:
            self.teams[nameSymbolB] = TeamStats(nameSymbolB)
        self.teams[nameSymbolB].addPerformance(game)

    def addPerformances(self, games):
        for game in games:
            self.addPerformance(game)

    def printGames(self):
        for team in self.teams:
            print(teamDict[team] + " Games:")
            self.teams[team].printGames()