import requests
import csv
from bs4 import BeautifulSoup
from player import Player
from player import GetHeaders

filename = 'playerdata.csv'

r = requests.get('https://fplform.com/fpl-player-data')

soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find('table', id='playerdata')
tablebody = soup.find('tbody')
rows = table.find_all('tr')

with open(filename, 'w', encoding='UTF8', newline='') as f:
  w = csv.writer(f)
  w.writerow(GetHeaders())

  for row in rows[1:-2]:
    player = Player(row)
    w.writerow(player.get_info())




