"""
database.py manages the database for the NFL games
"""

import sqlite3
import numpy as np
from multipledispatch import dispatch

class Database():
    def __init__(self):
        self.gameConnection = sqlite3.connect('games.db')
        self.gameCursor = self.gameConnection.cursor()
        self.createGamesTable()

    def createGamesTable(self):
        self.gameCursor.execute("""
        CREATE TABLE IF NOT EXISTS "Games" (
            "GameID"	INTEGER,
            "Date"	TEXT,
            "Home_Team"	TEXT,
            "Home_PassAtts"	INTEGER,
            "Home_Cmp"	INTEGER,
            "Home_FirstDowns"	INTEGER,
            "Home_FourthDownConv"	INTEGER,
            "Home_FourthDownConvLost"	INTEGER,
            "Home_Fumbles"	INTEGER,
            "Home_FumblesLost"	INTEGER,
            "Home_INTs"	INTEGER,
            "Home_Location"	TEXT,
            "Home_NetPassYds"	INTEGER,
            "Home_Outcome"	TEXT,
            "Home_PassingTDs"	INTEGER,
            "Home_PassYds"	INTEGER,
            "Home_Penalties"	INTEGER,
            "Home_PenaltyYds"	INTEGER,
            "Home_RushAtts"	INTEGER,
            "Home_RushingTDs"	INTEGER,
            "Home_RushingYds"	INTEGER,
            "Home_Sacked"	INTEGER,
            "Home_SackedYds"	INTEGER,
            "Home_Score"	INTEGER,
            "Home_ThirdDownConv"	INTEGER,
            "Home_ThirdDownConvLost"	INTEGER,
            "Home_TimeOfPoss"	INTEGER,
            "Home_TotalYds"	INTEGER,
            "Home_Turnovers"	INTEGER,
            "Away_Team"	TEXT,
            "Away_PassAtts"	INTEGER,
            "Away_Cmp"	INTEGER,
            "Away_FirstDowns"	INTEGER,
            "Away_FourthDownConv"	INTEGER,
            "Away_FourthDownConvLost"	INTEGER,
            "Away_Fumbles"	INTEGER,
            "Away_FumblesLost"	INTEGER,
            "Away_INTs"	INTEGER,
            "Away_Location"	TEXT,
            "Away_NetPassYds"	INTEGER,
            "Away_Outcome"	TEXT,
            "Away_PassingTDs"	INTEGER,
            "Away_PassYds"	INTEGER,
            "Away_Penalties"	INTEGER,
            "Away_PenaltyYds"	INTEGER,
            "Away_RushAtts"	INTEGER,
            "Away_RushingTDs"	INTEGER,
            "Away_RushingYds"	INTEGER,
            "Away_Sacked"	INTEGER,
            "Away_SackedYds"	INTEGER,
            "Away_Score"	INTEGER,
            "Away_ThirdDownConv"	INTEGER,
            "Away_ThirdDownConvLost"	INTEGER,
            "Away_TimeOfPoss"	INTEGER,
            "Away_TotalYds"	INTEGER,
            "Away_Turnovers"	INTEGER,
            PRIMARY KEY("GameID" AUTOINCREMENT)
        );
        """)
        self.gameConnection.commit()

    def addGame(self, date, stats):
        if stats[list(stats.keys())[0]]["Location"] == "Home":
            homeTeamSymbol = list(stats.keys())[0]
            awayTeamSymbol = list(stats.keys())[1]
            homeTeam = stats[homeTeamSymbol]
            awayTeam = stats[awayTeamSymbol]
        else:
            homeTeamSymbol = list(stats.keys())[1]
            awayTeamSymbol = list(stats.keys())[0]
            homeTeam = stats[homeTeamSymbol]
            awayTeam = stats[awayTeamSymbol]
        try:
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
            VALUES ({"?, " * (2 * len(homeTeam.values()) + 2) + "?"})
            """, [date, homeTeamSymbol] + list(homeTeam.values()) + [awayTeamSymbol] + list(awayTeam.values()))
            self.gameConnection.commit()
        except:
            print(f"Error adding game on {date}")

    @dispatch(int)
    def getGame(self, gameID):
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE GameID = {gameID}
        """)
        return self.gameCursor.fetchone()

    @dispatch(str, int)
    def getGame(self, date, index):
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date = "{date}"
        """)
        return self.gameCursor.fetchall()[index]

    @dispatch(str)
    def getGames(self, date):
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date = "{date}"
        """)
        return self.gameCursor.fetchall()

    @dispatch(int, int)
    def getGames(self, gameIDLower, gameIDUpper):
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE GameID >= {gameIDLower} AND GameID <= {gameIDUpper}
        """)
        return self.gameCursor.fetchall()

    @dispatch(str, str)
    def getGames(self, dateLower, dateUpper):
        self.gameCursor.execute(f"""
        SELECT * FROM Games WHERE Date >= "{dateLower}" AND Date <= "{dateUpper}"
        """)
        return self.gameCursor.fetchall()