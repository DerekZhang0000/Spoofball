"""
main.py contains the to-do list for the project
"""

# Important: https://scholars.unh.edu/cgi/viewcontent.cgi?article=1472&context=honors
# TODO: Finish scraping data DONE
#       Convert to SQL instead of using csvs DONE
#       Redo team stats classes for new data
#           Team classes should contain historical data points, averages and statistics should be calculated on demand for a specific date
#           Average, range, min, max, std dev, confidence intervals, moving averages, etc.
#       Add ranking algorithm / data
#       Determine if individual player / team composition info is needed
#       Determine if any other info is needed
#       Add data visualization
# TODO: Minor things
#       Clean up, refactoring, documentation, etc.
#       Remove spaces from datatype names
# NOTE: Adding the game on 2021-12-18 causes an error since its HTML structure is different for some reason and I don't care enough to fix it
# NOTE: Negative values cause errors in scaping data
# 202110030nwe.htm (New England Patriots have -1 rushing yards)
# 202201020chi.htm (New York Giants have -6 passing yards)
