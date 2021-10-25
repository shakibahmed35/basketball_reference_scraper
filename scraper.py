import requests
from bs4 import BeautifulSoup
import csv

headers = ["name", "team", "pos", "age", "games", "gamesStarted", "mpg", "fgm", "fga", "fg%", "3pm", "3pa", "3%", 
    "2%", "efg%", "ftm", "fta", "ft%", "orb", "drb", "trb", "apg", "spg", "bpg", "tov", "pf", "ppg"]



year = 1980
while year <= 2021:
    URL = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    filename = "./per_game_stats/" + str(year) + "per_game_stats.csv"

    f = open(filename, 'w')

    writer = csv.writer(f) 
    writer.writerow(headers)
    page = requests.get(URL)


    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="all_per_game_stats")
    players = results.find_all("tr", class_="full_table")




    for player in players:
        player_position = player.find("td", class_="center").text
        player_lefts = player.find_all("td", class_="left")
        player_name = player_lefts[0].text
        player_team = player_lefts[1].text
        player_rights = player.find_all("td", class_="right")
        player_age = player_rights[0].text
        player_games = player_rights[1].text
        player_games_started = player_rights[2].text
        player_mpg = player_rights[3].text
        player_fg_made = player_rights[4].text
        player_fga = player_rights[5].text
        player_fg_percentage = player_rights[6].text
        player_fg3_made = player_rights[7].text
        player_fg3_a = player_rights[8].text
        player_fg3_percent = player_rights[9].text
        player_fg2_percent = player_rights[12].text
        player_effect_fg_percent = player_rights[13].text
        player_ft_made = player_rights[14].text
        player_ft_attempted = player_rights[15].text
        player_ft_percentage = player_rights[16].text
        player_o_rebounds = player_rights[17].text
        player_d_reb = player_rights[18].text
        player_t_reb = player_rights[19].text
        player_assists = player_rights[20].text
        player_steals = player_rights[21].text
        player_blocks = player_rights[22].text
        player_tov = player_rights[23].text
        player_pf = player_rights[24].text
        player_pts = player_rights[25].text
        # Silly man writes bad code
        stats = [player_name, player_team, player_position, player_age, player_games, player_games_started, player_mpg, player_fg_made, player_fga,
        player_fg_percentage, player_fg3_made, player_fg3_a, player_fg3_percent, player_fg2_percent, player_effect_fg_percent, player_ft_made,
        player_ft_attempted, player_ft_percentage, player_o_rebounds, player_d_reb, player_t_reb, player_assists, player_steals, player_blocks,
        player_tov, player_pf, player_pts]
        writer.writerow(stats)
    year += 1


f.close()
    