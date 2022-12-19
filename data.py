import pandas as pd
import numpy as np
import csv
import glob
import random

from teamStats import TeamStats

dfs = []

for filename in glob.glob("data/*.csv"):
    df = pd.read_csv(filename, index_col=None, header=0)
    dfs.append(df)

games = pd.concat(dfs, axis=0, ignore_index=True)
teamNames = np.unique(np.append(games["Winner/tie"].unique(), games["Loser/tie"].unique()))
teams = {}
for team in teamNames:
    teams[team] = TeamStats(team)


f = open('gameStats.csv', 'w')
writer = csv.writer(f, lineterminator="\n")

columnNames = ["TeamA", "TeamB",
                # Team A Stats
                "WinPctA", "AvgScoreA", "AvgOppScoreA", "AvgYardsA", "AvgOppYardsA", "AvgTOA", "AvgOppTOA", "AvgWinMarginA", "AvgLossMarginA",
                "AvgScoreDiffA", "WinStreakA", "LossStreakA", "GamesPlayedA",
                # Team A Stats vs Team B
                "AvsBPct", "AvgScoreAvsB", "AvgOppScoreAvsB", "AvgYardsAvsB", "AvgOppYardsAvsB", "AvgTOAvsB", "AvgOppTOAvsB", "AvgWinMarginAvsB",
                "AvgLossMarginAvsB", "AvgScoreDiffAvsB", "WinStreakAvsB", "LossStreakAvsB", "GamesPlayedAvsB",
                # Team B Stats
                "WinPctB", "AvgScoreB", "AvgOppScoreB", "AvgYardsB", "AvgOppYardsB", "AvgTOB", "AvgOppTOB", "AvgWinMarginB", "AvgLossMarginB",
                "AvgScoreDiffB", "WinStreakB", "LossStreakB", "GamesPlayedB",
                # Outcome (W or L)
                "Outcome"]
writer.writerow(columnNames)

for index, row in games.iterrows():
    rowList = row.tolist()
    teamA, teamB = random.sample([rowList[0], rowList[1]], 2)
    outcome = "W" if teamA == row[0] else "L"

    # TODO: REPLACE IN SPREADSHEET INSTEAD OF THIS
    if teamA in ["Washington Redskins", "Washington Football Team"]:
        teamA = "Washington Commanders"
    elif teamB in ["Washington Redskins", "Washington Football Team"]:
        teamB = "Washington Commanders"

    teamAStats = teams[teamA]
    teamBStats = teams[teamB]
    statRow = [sorted(teams).index(teamA), sorted(teams).index(teamB)]
    statRow.extend(teamAStats.getStats())
    statRow.extend(teamAStats.getStatsVS(teamB))
    statRow.extend(teamBStats.getStats())
    statRow.extend(outcome)
    writer.writerow(statRow)

    teamAWins = True if teamA == row[0] else False
    teamAScore = rowList[2] if teamAWins else rowList[3]
    teamBScore = rowList[2] if not teamAWins else rowList[3]

    if teamAWins:            # Win Score,  Loss Score, Win Yards,  Loss Yards, Win TO,     Loss TO,    Opponent
        teamAStats.updateStats(teamAScore, teamBScore, rowList[4], rowList[5], rowList[6], rowList[7], teamB)
        teamBStats.updateStats(teamBScore, teamAScore, rowList[6], rowList[7], rowList[4], rowList[5], teamA)
    else:
        teamAStats.updateStats(teamAScore, teamBScore, rowList[6], rowList[7], rowList[4], rowList[5], teamB)
        teamBStats.updateStats(teamBScore, teamAScore, rowList[4], rowList[5], rowList[6], rowList[7], teamA)

f.close()