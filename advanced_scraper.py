import requests
from bs4 import BeautifulSoup
import csv


year = 1980
while year <= 2021:
    type_of_stat = "advanced"
    URL = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_" + type_of_stat + ".html"
    filename = "./" + type_of_stat + "_stats/" + str(year) + type_of_stat + "_stats.csv"

    f = open(filename, 'w')

    writer = csv.writer(f)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="all_advanced_stats")
    players = results.find_all("tr", class_="full_table")

    # Generating Headers
    headers = []
    for element in players[0].find_all():
        headers.append(element.get("data-stat"))
    writer.writerow(headers)


    for player in players:
        all_stats = player.find_all()
        stats = []
        for element in all_stats:
            stats.append(element.text)
        writer.writerow(stats)

    f.close()
    year += 1

