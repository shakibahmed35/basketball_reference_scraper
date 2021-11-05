import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from io import StringIO
import boto3

session = boto3.Session(
aws_access_key_id='AKIAQRSW4TINAC73XG2U',
aws_secret_access_key='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'
)

s3 = session.client('s3')

with open("./game_logs", "r") as f:
    game_urls = list(csv.reader(f))[0]
# Delete this when its time
game_urls = game_urls

# generates headeres given a basic tables header list
# Simply use code       headers = headers_generate(basic1_rows[1]) for basic// headers = headers_generate(advanced1_rows[1]) for advanced
def headers_generate(tr):
    headers = ["Player", "Team"]
    rows = tr.find_all("th")
    rows.pop(0)
    for row in rows:
        headers.append(row.text)
    return headers

# Generate player stats for the game for a given team
# to use code                team1_basic_table = table_generate(basic1_rows[2:])
def table_generate(trs, team):
    table = []
    for tr in trs:
        player = tr.find("th")
        data = [player.text]
        tds = tr.find_all("td")
        for td in tds:
            data.append(td.text)
        data.insert(1, team)
        table.append(data)
    table.pop(5)
    table.pop(-1)
    return table

# for url in game_urls:
# There will be a for loop to iterate through
for url in game_urls:
    current_url = "https://www.basketball-reference.com/" + url
    print(url)


    page = requests.get(current_url)
    soup = BeautifulSoup(page.content, "html.parser")


    all_tables = soup.find(id="content")
    four_tables = all_tables.find_all(class_="table_container")

    if(len(four_tables) != 4):
        continue
    team1_basic = four_tables[0]
    team1_advanced = four_tables[1]
    team2_basic = four_tables[2]
    team2_advanced = four_tables[3]

    team_name_1 = team1_basic.get("id")[8:11]
    team_name_2 = team2_basic.get("id")[8:11]
    # /boxscores/198310280DEN.html
    date = url[11:19]
    dir_name = team_name_1 + team_name_2 + date

    # Team 1
    basic1_rows = team1_basic.find_all("tr")
    # Generate basic headers
    basic_headers = headers_generate(basic1_rows[1])
    # Generate Team 1s basic table
    team1_basic_stats_table = table_generate(basic1_rows[2:], team_name_1)

    advanced1_rows = team1_advanced.find_all("tr")
    # Generate Advanced headers
    advanced_headers = headers_generate(advanced1_rows[1])
    # Generate Team 1s advanced table
    team1_advanced_stats_table = table_generate(advanced1_rows[2:], team_name_1)

    # Generate the two dataframes
    t1_basic_df = pd.DataFrame(team1_basic_stats_table, columns=basic_headers)
    t1_advanced_df = pd.DataFrame(team1_advanced_stats_table, columns=advanced_headers)
    t1_advanced_df.drop(columns=['Player', 'MP', 'Team'], inplace=True)
    team_1_fn = "./" + dir_name + "/" + team_name_1 + "_box_score.csv"
    t1_df = t1_basic_df.join(t1_advanced_df)
    t1_df.fillna(0, inplace=True)
    # t1 df now complete
    t1_csv_buffer = StringIO()
    t1_df.to_csv(t1_csv_buffer)
    t1_filename = f'boxscores/{dir_name}/{team_name_1}stats.csv'
    res = s3.put_object(Body=t1_csv_buffer.getvalue(), Bucket='awscse575', Key=t1_filename)


    # Team 2
    basic2_rows = team2_basic.find_all("tr")
    # Generate basic headers
    basic_headers = headers_generate(basic2_rows[1])
    # Generate Team 2s basic table
    team2_basic_stats_table = table_generate(basic2_rows[2:], team_name_2)

    advanced2_rows = team2_advanced.find_all("tr")
    # Generate Advanced headers
    advanced_headers = headers_generate(advanced2_rows[1])
    # Generate Team 2s advanced table
    team2_advanced_stats_table = table_generate(advanced2_rows[2:], team_name_2)

    # Generate the two dataframes
    t2_basic_df = pd.DataFrame(team2_basic_stats_table, columns=basic_headers)
    t2_advanced_df = pd.DataFrame(team2_advanced_stats_table, columns=advanced_headers)
    t2_advanced_df.drop(columns=['Player', 'MP', 'Team'], inplace=True)
    team_2_fn = "./" + dir_name + "/" + team_name_2 + "_box_score.csv"
    t2_df = t2_basic_df.join(t2_advanced_df)
    t2_df.fillna(0, inplace=True)
    # t2 df now complete
    t2_csv_buffer = StringIO()
    t2_df.to_csv(t2_csv_buffer)
    t2_filename = f'boxscores/{dir_name}/{team_name_2}stats.csv'
    res = s3.put_object(Body=t2_csv_buffer.getvalue(), Bucket='awscse575', Key=t2_filename)

