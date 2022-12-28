"""
scraper.py is used for scraping data from pro-football-reference.com
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from numpy import datetime64

url = "https://www.pro-football-reference.com"

def makeDriver() -> webdriver.Chrome:
    """Creates a Chrome webdriver with Selenium."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def getHrefs(year : str) -> list[str]:
    """Gets all the game links for a given year."""
    driver = makeDriver()
    driver.get(f"{url}/years/{year}/games.htm")
    return driver.execute_script("""
    function getHrefs() {
        let hrefs = [];
        let games = document.getElementsByTagName("tbody")[document.getElementsByTagName("tbody").length - 1].children;

        for (let i = 0; i < games.length; i++) {
            let game = games[i].children[7].children[0];
            if (game !== undefined && game.hasAttribute("href")) {
                hrefs.push(game.getAttribute("href"));
            }
        }

        return hrefs;
    }

    return getHrefs()
    """)

def getGameStats(gameLinks : list[str]) -> list[dict[str, dict[str, object]]]:
    """Returns the stat dictionaries for teams playing given a list of game links."""
    # NOTE: Negative values causes errors splitting on "-"s, though this is rare
    driver = makeDriver()
    stats = []
    try:
        for gameLink in gameLinks:
            driver.get(f"{url}{gameLink}")
            stats.append(driver.execute_script("""
            function isNumeric(str) {
                return /[[0-9]|-]/.test(str);
            }

            function splitStat(stat) {
                if (stat == "Rush-Yds-TDs") {
                    return ["Rushes", "Rushing Yds", "Rushing TDs"];
                }
                else if (stat == "Cmp-Att-Yd-TD-INT") {
                    return ["Cmp", "Att", "Passing Yds", "Passing TDs", "INT"];
                }
                else if (stat == "Sacked-Yards") {
                    return ["Sacked", "Sacked Yards"];
                }
                else if (stat == "Fumbles-Lost") {
                    return ["Fumbles", "Fumbles Lost"];
                }
                else if (stat == "Penalties-Yards") {
                    return ["Penalties", "Penalty Yds"];
                }
                else if (stat == "Third Down Conv.") {
                    return ["Third Down Conv.", "Third Down Conv. Lost"];
                }
                else if (stat == "Fourth Down Conv.") {
                    return ["Fourth Down Conv.", "Fourth Down Conv. Lost"];
                }
                else if (isNumeric(stat)) {
                    if (stat.includes(":")) {
                        let timeSplit = stat.split(":");
                        return [parseInt(timeSplit[0]) * 60 + parseInt(timeSplit[1])];
                    }
                    else {
                        let scoreSplit = stat.split("-");
                        let scores = [];
                        for (score of scoreSplit) {
                            scores.push(parseInt(score));
                        }

                        return scores
                    }
                }
                else {
                    return [stat];
                }
            }

            function getGameStats() {
                let teamA = document.getElementsByTagName("thead")[5].children[0].children[1].innerText;
                let teamB = document.getElementsByTagName("thead")[5].children[0].children[2].innerText;
                let statRows = document.getElementsByTagName("thead")[5].parentElement.children[3];
                let stats = {};
                let tableSections = document.getElementsByClassName("right");
                let teamAScore = parseInt(tableSections[tableSections.length - 5].innerText);
                let teamBScore = parseInt(tableSections[tableSections.length - 4].innerText);

                stats[teamA] = {"Score" : teamAScore,
                                "Outcome" : teamAScore > teamBScore ? "W" : "L",
                                "Location" : "Away"};
                stats[teamB] = {"Score" : teamBScore,
                                "Outcome" : teamBScore > teamAScore ? "W" : "L",
                                "Location" : "Home"};

                for (let i = 0; i < statRows.children.length; i++) {
                    let statNameSplit = splitStat(statRows.children[i].children[0].innerText);
                    let teamAScoreSplit = splitStat(statRows.children[i].children[1].innerText);
                    let teamBScoreSplit = splitStat(statRows.children[i].children[2].innerText);

                    for (let j = 0; j < statNameSplit.length; j++) {
                        stats[teamA][statNameSplit[j]] = teamAScoreSplit[j];
                        stats[teamB][statNameSplit[j]] = teamBScoreSplit[j];
                    }
                }

                return stats
            }

            return getGameStats()
            """))
    except:
        # Loop will error out if the game has not taken place yet
        driver.close()
    return stats

def getDate(gameLink : str) -> str:
    """Gets the date of a given game link."""
    date = gameLink.split("/")[2]
    return f"{date[0:4]}-{date[4:6]}-{date[6:8]}"

def getYear(date : str) -> str:
    """Gets the year of a given game link."""
    return date.split("-")[0]

def beforeDate(date : str, beforeDate : str) -> bool:
    """Returns whether the date (YYYY-MM-DD) is before the beforeDate, inclusive."""
    return datetime64(date) < datetime64(beforeDate)

def afterDate(date : str, afterDate : str) -> bool:
    """Returns whether the date (YYYY-MM-DD) is after the afterDate, inclusive."""
    return datetime64(date) > datetime64(afterDate)