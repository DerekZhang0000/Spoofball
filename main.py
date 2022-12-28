"""
main.py contains the to-do list for the project
"""

# Important: https://scholars.unh.edu/cgi/viewcontent.cgi?article=1472&context=honors
# TODO: Finish scraping data DONE
#       Convert to SQL instead of using CSVs DONE
#       Add way to make predictions
#       Redo team stats classes for new data
#           Team classes should contain historical data points, averages and statistics should be calculated on demand for a specific date
#           Averages DONE, confidence intervals, moving averages, win margin, loss margin, etc.
#       Add way to update database with scraper DONE
#       Add way to populate empty database
#       Add ranking algorithm / data
#       Determine if individual player / team composition info is needed
#       Determine if any other info is needed
#       Add data visualization / simulation
# TODO: Minor things
#       Replace lists with numpy arrays DONE
#       Clean up, refactoring, documentation, etc. Done for now
#       Remove spaces from datatype names DONE
#       Find a way to avoid tuple / list conversion
#       Add a better way to get the current date and update the database accordingly
# NOTE: Adding the game on 2021-12-18 causes an error since its HTML structure is different for some reason and I don't care enough to fix it
# NOTE: Negative values cause errors in scaping data
# 202110030nwe.htm (New England Patriots have -1 rushing yards)
# 202201020chi.htm (New York Giants have -6 passing yards)
