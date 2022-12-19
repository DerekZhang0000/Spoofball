from collections import defaultdict

class VersusStats():
    # Class containing the statistics for a team against a specific opponent
    def __init__(self, oppName):
        self.name = oppName
        self.winPct = 0
        self.avgScore = 0
        self.avgOppScore = 0
        self.avgYards = 0
        self.avgOppYards = 0
        self.avgTO = 0
        self.avgOppTO = 0
        self.avgWinMargin = 0
        self.avgLossMargin = 0
        self.avgScoreDiff = 0
        self.winStreak = 0
        self.lossStreak = 0
        self.gamesPlayed = 0

    def updateStats(self, score, oppScore, yards, TO, oppYards, oppTO):
        self.gamesPlayed += 1
        self.winPct = (self.winPct * (self.gamesPlayed - 1) + int(score > oppScore)) / self.gamesPlayed
        self.avgScore = (self.avgScore * (self.gamesPlayed - 1) + score) / self.gamesPlayed
        self.avgOppScore = (self.avgOppScore * (self.gamesPlayed - 1) + oppScore) / self.gamesPlayed
        self.avgYards = (self.avgYards * (self.gamesPlayed - 1) + yards) / self.gamesPlayed
        self.avgOppYards = (self.avgOppYards * (self.gamesPlayed - 1) + oppYards) / self.gamesPlayed
        self.avgTO = (self.avgTO * (self.gamesPlayed - 1) + TO) / self.gamesPlayed
        self.avgOppTO = (self.avgOppTO * (self.gamesPlayed - 1) + oppTO) / self.gamesPlayed
        self.avgWinMargin = (self.avgWinMargin * (self.gamesPlayed - 1) + max(score - oppScore, 0)) / self.gamesPlayed
        self.avgLossMargin = (self.avgLossMargin * (self.gamesPlayed - 1) + max(oppScore - score, 0)) / self.gamesPlayed
        self.avgScoreDiff = (self.avgScoreDiff * (self.gamesPlayed - 1) + (score - oppScore)) / self.gamesPlayed

        if score > oppScore:
            self.winStreak += 1
            self.lossStreak = 0
        else:
            self.lossStreak += 1
            self.winStreak = 0

    def getStats(self):
        return [self.winPct, self.avgScore, self.avgOppScore, self.avgYards, self.avgOppYards, self.avgTO, self.avgOppTO,
                self.avgWinMargin, self.avgLossMargin, self.avgScoreDiff, self.winStreak, self.lossStreak, self.gamesPlayed]

class TeamStats():
    # Class containing the statistics for a team
    def __init__(self, name):
        self.name = name
        self.winPct = 0
        self.avgScore = 0
        self.avgOppScore = 0
        self.avgYards = 0
        self.avgOppYards = 0
        self.avgTO = 0
        self.avgOppTO = 0
        self.avgWinMargin = 0
        self.avgLossMargin = 0
        self.avgScoreDiff = 0
        self.winStreak = 0
        self.lossStreak = 0
        self.gamesPlayed = 0
        self.vsStats = defaultdict(VersusStats)

    def updateStats(self, score, oppScore, yards, TO, oppYards, oppTO, oppName):
        self.gamesPlayed += 1
        self.winPct = (self.winPct * (self.gamesPlayed - 1) + int(score > oppScore)) / self.gamesPlayed
        self.avgScore = (self.avgScore * (self.gamesPlayed - 1) + score) / self.gamesPlayed
        self.avgOppScore = (self.avgOppScore * (self.gamesPlayed - 1) + oppScore) / self.gamesPlayed
        self.avgYards = (self.avgYards * (self.gamesPlayed - 1) + yards) / self.gamesPlayed
        self.avgOppYards = (self.avgOppYards * (self.gamesPlayed - 1) + oppYards) / self.gamesPlayed
        self.avgTO = (self.avgTO * (self.gamesPlayed - 1) + TO) / self.gamesPlayed
        self.avgOppTO = (self.avgOppTO * (self.gamesPlayed - 1) + oppTO) / self.gamesPlayed
        self.avgWinMargin = (self.avgWinMargin * (self.gamesPlayed - 1) + (score - oppScore)) / self.gamesPlayed
        self.avgLossMargin = (self.avgLossMargin * (self.gamesPlayed - 1) + (oppScore - score)) / self.gamesPlayed
        self.avgScoreDiff = (self.avgScoreDiff * (self.gamesPlayed - 1) + (score - oppScore)) / self.gamesPlayed

        if score > oppScore:
            self.winStreak += 1
            self.lossStreak = 0
        else:
            self.winStreak = 0
            self.lossStreak += 1
        if oppName not in self.vsStats:
            self.vsStats[oppName] = VersusStats(oppName)

        self.vsStats[oppName].updateStats(score, oppScore, yards, TO, oppYards, oppTO)

    def getStats(self):
        return [self.winPct, self.avgScore, self.avgOppScore, self.avgYards, self.avgOppYards, self.avgTO, self.avgOppTO,
                self.avgWinMargin, self.avgLossMargin, self.avgScoreDiff, self.winStreak, self.lossStreak, self.gamesPlayed]

    def getStatsVS(self, oppName):
        if oppName not in self.vsStats:
            return [0] * 13
        else:
            return self.vsStats[oppName].getStats()