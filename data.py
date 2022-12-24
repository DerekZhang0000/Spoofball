"""
data.py is used to compile data from the scraper into the database
"""

from database import Database
from scraper import *

db = Database()

def beforeDate(date, beforeDate):
    # Returns whether the date (YYYY-MM-DD) is before the beforeDate (exclusive)
    if int(date[:4]) < int(beforeDate[:4]):
        return True
    elif int(date[:4]) > int(beforeDate[:4]):
        return False
    elif int(date[:4]) == int(beforeDate[:4]):
        if int(date[5:7]) < int(beforeDate[5:7]):
            return True
        elif int(date[5:7]) > int(beforeDate[5:7]):
            return False
        elif int(date[5:7]) == int(beforeDate[5:7]):
            return int(date[8:10]) < int(beforeDate[8:10])

def afterDate(date, afterDate):
    # Returns whether the date (YYYY-MM-DD) is after the afterDate (exclusive)
    if int(date[:4]) > int(afterDate[:4]):
        return True
    elif int(date[:4]) < int(afterDate[:4]):
        return False
    elif int(date[:4]) == int(afterDate[:4]):
        if int(date[5:7]) > int(afterDate[5:7]):
            return True
        elif int(date[5:7]) < int(afterDate[5:7]):
            return False
        elif int(date[5:7]) == int(afterDate[5:7]):
            return int(date[8:10]) > int(afterDate[8:10])

for year in [2021, 2022]:
    for href in getHrefs(year):
        date = getDate(href)
        if beforeDate(date, "2022-12-24") and afterDate(date, "2021-12-18"):
            db.addGame(getDate(href), getTeamStats(href))

# for href in getHrefs(2022):
#     db.addGame(getDate(href), getTeamStats(href))

# db.gameCursor.execute("""DELETE FROM Games WHERE GameID >= 1013""")
# db.gameConnection.commit()