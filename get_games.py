import requests
from bs4 import BeautifulSoup, SoupStrainer
import csv

type_of_stat = "games"
months = ["-october", "-november", "-december", "-january", "-february", "-march", "-april", "-may", "-june", "-july"]
game_urls = []
year = 1980
while year <= 2021:
    for month in months:
        try:
            URL = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_" + type_of_stat + month + ".html"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="all_schedule")
            games = results.find_all("tr")
            for game in games:
                all_things = game.find_all("td", class_="center")
                for thing in all_things:
                    if thing.get("data-stat") == "box_score_text":
                        a = thing.find("a")
                        game_urls.append(a.get("href"))
        except AttributeError:
            print("month does'nt exist")
    print(year)
    year += 1

with open("./game_logs", "w") as f:
    writer = csv.writer(f)
    writer.writerow(game_urls)
    

