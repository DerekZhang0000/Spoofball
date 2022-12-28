"""
stats.py contains classes for storing and calculating stats
"""

import numpy as np

from teams import teamDict
from collections import defaultdict

statsDataType = np.dtype([("Date", "datetime64[D]"), ("OppNameSymbol", "U3"), ("PassAtts", np.ubyte), ("Completions", np.ubyte),
                          ("FirstDowns", np.ubyte), ("4thConv", np.ubyte), ("4thConvLost", np.ubyte), ("Fumbles", np.ubyte),
                          ("FumblesLost", np.ubyte), ("Interceptions", np.ubyte), ("Location", "U4"), ("NetPassYards", np.ushort),
                          ("Outcome", "U1"), ("PassTDs", np.ubyte), ("PassYards", np.ushort), ("Penalties", np.ubyte),
                          ("PenaltyYards", np.ushort), ("RushAtts", np.ubyte), ("RushTDs", np.ubyte), ("RushYards", np.ushort),
                          ("Sacks", np.ubyte), ("SackYards", np.ushort), ("Score", np.ubyte), ("3rdConv", np.ubyte),
                          ("3rdConvLost", np.ubyte), ("TimeOfPoss", np.ushort), ("TotalYards", np.ushort), ("Turnovers", np.ubyte)])

vsStatsDataType = np.dtype([("Date", "datetime64[D]"), ("PassAtts", np.ubyte), ("Completions", np.ubyte), ("FirstDowns", np.ubyte),
                            ("4thConv", np.ubyte), ("4thConvLost", np.ubyte), ("Fumbles", np.ubyte), ("FumblesLost", np.ubyte),
                            ("Interceptions", np.ubyte), ("Location", "U4"), ("NetPassYards", np.ushort), ("Outcome", "U1"),
                            ("PassTDs", np.ubyte), ("PassYards", np.ushort), ("Penalties", np.ubyte), ("PenaltyYards", np.ushort),
                            ("RushAtts", np.ubyte), ("RushTDs", np.ubyte), ("RushYards", np.ushort), ("Sacks", np.ubyte),
                            ("SackYards", np.ushort), ("Score", np.ubyte), ("3rdConv", np.ubyte), ("3rdConvLost", np.ubyte),
                            ("TimeOfPoss", np.ushort), ("TotalYards", np.ushort), ("Turnovers", np.ubyte)])

class VersusStats():
    """Class containing the statistics for a team against a specific opponent."""
    def __init__(self, oppNameSymbol : str) -> None:
        self.nameSymbol = oppNameSymbol                         # Name of the opponent
        self.performance = np.array([], dtype=vsStatsDataType)  # Array containing the performance data for each game

    def addPerformance(self, game : list) -> None:
        """Add a new performance to the teams' stats."""
        performance = np.array(game, dtype=vsStatsDataType)
        self.performance = np.append(self.performance, performance)

    def getHistoricalStats(self, date : np.datetime64) -> np.array:
        """Get the stats for a specific date."""
        games = self.performance
        statPoint = np.array([])
        gamesBeforeDate = games[games["Date"] <= date]

        for stat in vsStatsDataType.names:
            # Generate stat averages
            if stat in ("Date", "Outcome", "Location"):
                continue
            statPoint = np.append(statPoint, np.average(gamesBeforeDate[stat]))

        statPoint = np.append(statPoint, (len(gamesBeforeDate[gamesBeforeDate["Outcome"] == "W"]) / len(gamesBeforeDate)))   # Win percentage against opponent

        return statPoint

    def getPredictionStats(self) -> np.array:
        """Get the current stats for all games."""
        games = self.performance
        statPoint = np.array([])

        for stat in vsStatsDataType.names:
            # Generate stat averages
            if stat in ("Date", "Outcome", "Location"):
                continue
            statPoint = np.append(statPoint, np.average(games[stat]))

        statPoint = np.append(statPoint, (len(games[games["Outcome"] == "W"]) / len(games)))    # Win percentage against opponent

        return statPoint

class TeamStats():
    """Class containing the statistics for a team."""
    def __init__(self, nameSymbol : str) -> None:
        self.nameSymbol = nameSymbol                            # Name of the team
        self.performance = np.array([], dtype=statsDataType)    # Array containing the performance data for each game
        self.vsPerformance = defaultdict(VersusStats)           # Dictionary containing the performance data for each opponent

    def addPerformance(self, game : list) -> None:
        """Add a new performance to the teams' stats."""
        # The indexes are semi-hardcoded, indexes 0 and 1 are the Game ID and the Date.
        # The rest of the data can be divided into 2 congruent groups, the team's and the opponent's.
        # The first index of each group is the team's name symbol.

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

    def getHistoricalStats(self) -> np.array:
        """Return the historical stats for the team."""
        stats = np.array([])
        games = self.performance

        for date in np.nditer(games["Date"]):
            statPoint = np.array([])
            gamesBeforeDate = games[games["Date"] <= date]
            gameOnDate = games[games["Date"] == date]

            for stat in statsDataType.names:
                if stat in ("Date", "OppNameSymbol", "Outcome", "Location"):
                    continue
                # Generate stat averages
                statPoint = np.append(statPoint, np.average(games[games["Date"] <= date][stat]))

            statPoint = np.append(statPoint, len(gamesBeforeDate[gamesBeforeDate["Outcome"] == "W"]) / len(games[games["Date"] <= date]))   # Win percentage
            statPoint = np.append(statPoint, int(games[games["Date"] == date]["Location"] == "Home"))                                       # Team is home or not

            oppNameSymbol = gameOnDate["OppNameSymbol"].item()
            statPoint = np.append(statPoint, self.vsPerformance[oppNameSymbol].getHistoricalStats(date))    # Team VS Opponent stats
            statPoint = np.append(statPoint, int(gameOnDate["Outcome"] == "W"))                             # Win is the last element in the stat point for convenience

            stats = np.vstack([stats, statPoint]) if stats.size else statPoint

        return stats

    def getPredictionStats(self, oppNameSymbol : str) -> np.array:
        """Return the current stats for the team."""
        games = self.performance
        statPoint = np.array([])

        for stat in statsDataType.names:
            if stat in ("Date", "OppNameSymbol", "Outcome", "Location"):
                continue
            # Generate stat averages
            statPoint = np.append(statPoint, np.average(games[stat]))

        statPoint = np.append(statPoint, len(games[games["Outcome"] == "W"]) / len(games))  # Win percentage
        statPoint = np.append(statPoint, 1)                                                 # Home team is always the team being predicted

        statPoint = np.append(statPoint, self.vsPerformance[oppNameSymbol].getPredictionStats())    # Team VS Opponent stats

        return statPoint

    def printGames(self):
        """Print the games in the team's performance array."""
        for game in np.nditer(self.performance):
            print(game)

class statCEO():
    """Executive class for team stats."""
    def __init__(self) -> None:
        self.teams = defaultdict(TeamStats)    # Dictionary containing the stats for each team

    def addPerformance(self, game : list) -> None:
        """Add a new performance to a team's respective stats."""
        nameSymbolA = game[2]
        if nameSymbolA not in self.teams:
            self.teams[nameSymbolA] = TeamStats(nameSymbolA)
        self.teams[nameSymbolA].addPerformance(game)

        secondGroupIndex = int(((len(game) - 2) / 2) + 2)
        nameSymbolB = game[secondGroupIndex]
        if nameSymbolB not in self.teams:
            self.teams[nameSymbolB] = TeamStats(nameSymbolB)
        self.teams[nameSymbolB].addPerformance(game)

    def addPerformances(self, games : list[list]) -> None:
        """Add multiple performances to the team stats."""
        for game in games:
            self.addPerformance(game)

    def printGames(self) -> None:
        """Prints all the performances for each team."""
        for team in self.teams:
            print(teamDict[team] + " Games:")
            self.teams[team].printGames()

    def getHistoricalStats(self) -> np.array:
        """Returns the stats for all the teams."""
        teamStats = np.array([])
        for team in self.teams:
            teamStats = np.vstack([teamStats, self.teams[team].getHistoricalStats()]) if teamStats.size else self.teams[team].getHistoricalStats()
        return teamStats

    def getPredictionStats(self, homeNameSymbol : str, awayNameSymbol : str) -> np.array:
        """Returns the current stats for the home team."""
        teamStats = self.teams[homeNameSymbol].getPredictionStats(awayNameSymbol)

        return teamStats

    def getStatNames(self) -> np.array:
        """Returns the names of the stats."""
        statNames = np.array([])
        # Team Stats
        for stat in statsDataType.names:
            if stat in ("Date", "OppNameSymbol", "Outcome", "Location"):
                continue
            # Stat averages
            statNames = np.append(statNames, stat + "Avg")
        statNames = np.append(statNames, "Win Percentage")
        statNames = np.append(statNames, "Home")
        # Team VS Opponent Stats
        for stat in vsStatsDataType.names:
            if stat in ("Date", "Outcome", "Location"):
                continue
            statNames = np.append(statNames, stat + "VSAvg")
        statNames = np.append(statNames, "VSWinPercentage")
        # Win
        statNames = np.append(statNames, "Win")
        return statNames

    def paramCount(self) -> int:
        """Returns the number of stats."""
        return len(self.getStatNames())