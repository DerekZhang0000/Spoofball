"""
database.py manages the database for the NFL games
"""

import sqlite3
from teams import teamList

class Database():
    def __init__(self):
        self.gameConnection = sqlite3.connect('games.db')
        self.gameCursor = self.gameConnection.cursor()
        self.createGamesTable()

    def createGamesTable(self):
        self.gameCursor.execute("""
        CREATE TABLE IF NOT EXISTS Games (
            GameID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date,
            Home_Team,
            Home_Att,
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
            Home_Rushes,
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
            Away_Att,
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
            Away_Rushes,
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
                Home_Att,
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
                Home_Rushes,
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
                Away_Att,
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
                Away_Rushes,
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