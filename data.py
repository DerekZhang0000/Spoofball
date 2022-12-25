"""
data.py is used to compile data from the scraper into the database
"""

from database import Database
from teamStats import TeamStats
from scraper import *

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

def equalDate(date, equalDate):
    # Returns whether the date (YYYY-MM-DD) is equal to the equalDate
    return date == equalDate

db = Database()
stats = TeamStats("BUF")
# print(db.getGame("2020-09-13", 1))
stats.addPerformance(db.getGame("2020-09-13", 1))
print(stats.performance[0])