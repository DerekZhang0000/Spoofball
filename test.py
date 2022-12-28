"""
test.py is used for testing stuff
"""

# import matplotlib.pyplot as plt

# from odds import *

# X = [i / 100 for i in range(50, 100)]
# Y = [expectedTrueValue(pctToOdds(pct), pctToOdds(.82)) for pct in X]

# plt.plot(X, Y)
# plt.title("Expected True Value (.82) vs. Implied Probability")
# plt.xlabel("Implied Probability")
# plt.ylabel("Expected True Value")
# plt.show()

from database import Database

db = Database()
# db.updateDatabase()

from stats import statCEO
stats = statCEO()
stats.addPerformances(db.getGames(700, 1326))