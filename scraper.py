"""
scraper.py is used for scraping data from pro-football-reference.com
"""



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

url = "https://www.pro-football-reference.com"
year = 2020

def getHrefs(year):
    driver.get(f"{url}/years/{year}/games.htm")
    return driver.execute_script("""function getHrefs() {
    let hrefs = [];
    let games = document.getElementsByTagName("tbody")[document.getElementsByTagName("tbody").length - 1].children;
    for (let i = 0; i < games.length; i++) {
        let game = games[i].children[7].children[0];
        if (game !== undefined && game.hasAttribute("href")) {
            hrefs.push(game.getAttribute("href"));
        }
    }
    return hrefs
}
return getHrefs()""")

# TODO: Get game stats
# def getGameStats(game):
#     document.getElementsByTagName("thead")[5].children[0].children[1].innerText
#     document.getElementsByTagName("thead")[5].parentElement.children[3]
#     You can find out who is visitor and who is home here too