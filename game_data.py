import requests
from bs4 import BeautifulSoup
import csv

with open("./game_logs", "r") as f:
    game_urls = list(csv.reader(f))[0]

# for url in game_urls:
URL = "https://www.basketball-reference.com" + game_urls[0]
filename = "./game_data"
