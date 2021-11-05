from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests
import boto3

session = boto3.Session(
aws_access_key_id='AKIAQRSW4TINAC73XG2U',
aws_secret_access_key='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'
)

s3 = session.client('s3')

def get_roster(team,year):
  roster_page = requests.get(f'https://www.basketball-reference.com/teams/{team}/{year}.html')
  soup = BeautifulSoup(roster_page.content,'html.parser')

  roster_div = soup.find("div", {"id": "div_roster"})

  columns = [header.string for header in roster_div.thead.find_all('th')]

  roster = [[num.string] for num in roster_div.tbody.find_all('th')]

  for count,i in enumerate(range(0,len(roster_div.tbody.findAll('td')),8)):
    row = [roster_div.tbody.findAll('td')[i+j].string for j in range(8)]
    roster[count].extend(row)

  return pd.DataFrame(roster, columns=columns)

def send_rosters_to_s3(team_arr):
  for team in team_arr:
    for year in range(1984, 2022):
      try:
        roster = get_roster(team,year)
      except Exception as e:
        print(team,year, "DNE")
        continue

      #encoding the csv as a string
      csv_buffer = StringIO()
      roster.to_csv(csv_buffer)

      filename = f'rosters/{team}_{year}.csv'
      res = s3.put_object(Body=csv_buffer.getvalue(), Bucket='awscse575', Key=filename)

teams = ['ATL','BRK','BOS','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
ded_teams = ['NJN', 'VAN', 'SEA', 'KCK', 'WSB', 'CHH', 'CHO', 'SDC']

send_rosters_to_s3(teams)
send_rosters_to_s3(ded_teams)