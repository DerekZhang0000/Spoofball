"""
database.py manages the database for the NFL games
"""

import sqlite3

from scraper import *
from multipledispatch import dispatch

class Database():
    def __init__(self) -> None:
        self.gameConnection = sqlite3.connect('games.db')
        self.gameCursor = self.gameConnection.cursor()
        self.createGamesTable()

    def createGamesTable(self) -> None:
        """Creates the Games table if it does not exist."""
        self.gameCursor.execute("""
        CREATE TABLE IF NOT EXISTS "Games" (
        "GameID"	                INTEGER NOT NULL UNIQUE,
        "Date"	                    TEXT NOT NULL,
        "Home_Team"	                TEXT NOT NULL,
        "Home_PassAtts"	            INTEGER NOT NULL,
        "Home_Cmp"	                INTEGER NOT NULL,
        "Home_FirstDowns"	        INTEGER NOT NULL,
        "Home_FourthDownConv"	    INTEGER NOT NULL,
        "Home_FourthDownConvLost"	INTEGER NOT NULL,
        "Home_Fumbles"	            INTEGER NOT NULL,
        "Home_FumblesLost"	        INTEGER NOT NULL,
        "Home_INTs"	                INTEGER NOT NULL,
        "Home_Location"	            TEXT NOT NULL,
        "Home_NetPassYds"	        INTEGER NOT NULL,
        "Home_Outcome"	            TEXT NOT NULL,
        "Home_PassingTDs"	        INTEGER NOT NULL,
        "Home_PassYds"	            INTEGER NOT NULL,
        "Home_Penalties"	        INTEGER NOT NULL,
        "Home_PenaltyYds"	        INTEGER NOT NULL,
        "Home_RushAtts"	            INTEGER NOT NULL,
        "Home_RushingTDs"	        INTEGER NOT NULL,
        "Home_RushingYds"	        INTEGER NOT NULL,
        "Home_Sacked"	            INTEGER NOT NULL,
        "Home_SackedYds"	        INTEGER NOT NULL,
        "Home_Score"	            INTEGER NOT NULL,
        "Home_ThirdDownConv"	    INTEGER NOT NULL,
        "Home_ThirdDownConvLost"	INTEGER NOT NULL,
        "Home_TimeOfPoss"	        INTEGER NOT NULL,
        "Home_TotalYds"	            INTEGER NOT NULL,
        "Home_Turnovers"	        INTEGER NOT NULL,
        "Away_Team"	                TEXT NOT NULL,
        "Away_PassAtts"	            INTEGER NOT NULL,
        "Away_Cmp"	                INTEGER NOT NULL,
        "Away_FirstDowns"	        INTEGER NOT NULL,
        "Away_FourthDownConv"	    INTEGER NOT NULL,
        "Away_FourthDownConvLost"	INTEGER NOT NULL,
        "Away_Fumbles"	            INTEGER NOT NULL,
        "Away_FumblesLost"	        INTEGER NOT NULL,
        "Away_INTs"	                INTEGER NOT NULL,
        "Away_Location"	            TEXT NOT NULL,
        "Away_NetPassYds"	        INTEGER NOT NULL,
        "Away_Outcome"	            TEXT NOT NULL,
        "Away_PassingTDs"	        INTEGER NOT NULL,
        "Away_PassYds"	            INTEGER NOT NULL,
        "Away_Penalties"	        INTEGER NOT NULL,
        "Away_PenaltyYds"	        INTEGER NOT NULL,
        "Away_RushAtts"	            INTEGER NOT NULL,
        "Away_RushingTDs"	        INTEGER NOT NULL,
        "Away_RushingYds"	        INTEGER NOT NULL,
        "Away_Sacked"	            INTEGER NOT NULL,
        "Away_SackedYds"	        INTEGER NOT NULL,
        "Away_Score"	            INTEGER NOT NULL,
        "Away_ThirdDownConv"	    INTEGER NOT NULL,
        "Away_ThirdDownConvLost"	INTEGER NOT NULL,
        "Away_TimeOfPoss"	        INTEGER NOT NULL,
        "Away_TotalYds"	            INTEGER NOT NULL,
        "Away_Turnovers"	        INTEGER NOT NULL,
        PRIMARY KEY("GameID" AUTOINCREMENT)
        );
        """)
        self.gameConnection.commit()

    def addGame(self, date : str, statDict : dict[str, dict[str, object]]) -> None:
        """Adds a game to the database."""
        if statDict[list(statDict.keys())[0]]["Location"] == "Home":
            homeNameSymbol = list(statDict.keys())[0]
            awayNameSymbol = list(statDict.keys())[1]
            homeStats = statDict[homeNameSymbol]
            awayStats = statDict[awayNameSymbol]
        else:
            homeNameSymbol = list(statDict.keys())[1]
            awayNameSymbol = list(statDict.keys())[0]
            homeStats = statDict[homeNameSymbol]
            awayStats = statDict[awayNameSymbol]
        try:
            paramCount = (2 * len(homeStats.values()) + 3)
            self.gameCursor.execute(f"""
            INSERT INTO Games (
                Date,
                Home_Team,
                Home_PassAtts,
                Home_Cmp,
                Home_FirstDowns,
                Home_FourthDownConv,
                Home_FourthDownConvLost,
                Home_Fumbles,
                Home_FumblesLost,
                Home_INTs,
                Home_Location,
                Home_NetPassYds,
                Home_Outcome,
                Home_PassingTDs,
                Home_PassYds,
                Home_Penalties,
                Home_PenaltyYds,
                Home_RushAtts,
                Home_RushingTDs,
                Home_RushingYds,
                Home_Sacked,
                Home_SackedYds,
                Home_Score,
                Home_ThirdDownConv,
                Home_ThirdDownConvLost,
                Home_TimeOfPoss,
                Home_TotalYds,
                Home_Turnovers,
                Away_Team,
                Away_PassAtts,
                Away_Cmp,
                Away_FirstDowns,
                Away_FourthDownConv,
                Away_FourthDownConvLost,
                Away_Fumbles,
                Away_FumblesLost,
                Away_INTs,
                Away_Location,
                Away_NetPassYds,
                Away_Outcome,
                Away_PassingTDs,
                Away_PassYds,
                Away_Penalties,
                Away_PenaltyYds,
                Away_RushAtts,
                Away_RushingTDs,
                Away_RushingYds,
                Away_Sacked,
                Away_SackedYds,
                Away_Score,
                Away_ThirdDownConv,
                Away_ThirdDownConvLost,
                Away_TimeOfPoss,
                Away_TotalYds,
                Away_Turnovers
            )
            VALUES ({"?, " * (paramCount - 1) + "?"});
            """, [date, homeNameSymbol] + list(homeStats.values()) + [awayNameSymbol] + list(awayStats.values()))
            self.gameConnection.commit()
        except:
            print(f"Error adding {homeNameSymbol} vs {awayNameSymbol} game on {date}")

    def addGames(self, dates : list[str], statDicts : list[dict[str, dict[str, object]]]) -> None:
        """Adds multiple games to the database."""
        for dateStats in zip(dates, statDicts):
            date, statDict = dateStats
            self.addGame(date, statDict)

    def updateDatabase(self) -> None:
        """Updates the database with new games."""
        self.gameCursor.execute("""SELECT MAX(GameID) FROM Games;""")
        maxGameID = self.gameCursor.fetchone()[0]
        self.gameCursor.execute(f"""SELECT Date FROM Games WHERE GameID = {maxGameID};""")
        latestDate = self.gameCursor.fetchone()[0]
        self.gameCursor.execute(f"""SELECT COUNT(Date) FROM Games WHERE Date = "{latestDate}";""")
        numGames = self.gameCursor.fetchone()[0]
        newGameID = maxGameID - numGames
        # Games with the same date as the latest date are removed from the database and the game ID counter is adjusted
        # This is done to prevent duplicates from being added to the database
        self.gameCursor.execute(f"""DELETE FROM Games WHERE Date = "{latestDate}";""")
        self.gameConnection.commit()
        self.gameCursor.execute(f"""UPDATE sqlite_sequence SET seq = {newGameID};""")
        self.gameConnection.commit()

        gameLinks = getHrefs(getYear(latestDate))
        for gameLink in [gameLink for gameLink in gameLinks]:
            # Games with a date that is strictly less than the latest date are removed from the list of games to be added
            if beforeDate(getDate(gameLink), latestDate):
                gameLinks.remove(gameLink)
        dates = [getDate(gameLink) for gameLink in gameLinks]
        self.addGames(dates, getGameStats(gameLinks))

    @dispatch(int)
    def getGame(self, gameID : int) -> list:
        """Returns a game for a given game ID."""
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE GameID = {gameID};
        """)
        return list(self.gameCursor.fetchone())

    @dispatch(str, int)
    def getGame(self, date : str, index : int) -> list:
        """Returns a game for a given date and index."""
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date = "{date}";
        """)
        return list(self.gameCursor.fetchall()[index])

    @dispatch(str)
    def getGames(self, date : str) -> list[list]:
        """Returns a list of games for a given date."""
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date = "{date}";
        """)
        return [list(tup) for tup in list(self.gameCursor.fetchall())]

    @dispatch(int, int)
    def getGames(self, gameIDLower : int, gameIDUpper : int) -> list[list]:
        """Returns a list of games between the two game IDs, inclusive."""
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE GameID >= {gameIDLower} AND GameID <= {gameIDUpper};
        """)
        return [list(tup) for tup in list(self.gameCursor.fetchall())]

    @dispatch(str, str)
    def getGames(self, dateLower : str, dateUpper : str) -> list[list]:
        """Returns a list of games between the two dates, inclusive."""
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date >= "{dateLower}" AND Date <= "{dateUpper}";
        """)
        return [list(tup) for tup in list(self.gameCursor.fetchall())]