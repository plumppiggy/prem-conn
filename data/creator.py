from player import Player
from player import Team
import csv
import random


if __name__ == '__main__':
  teams = {}
  players = []
  # read the data from the csv
  with open('playerdata.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
      # covert the row to a player
      player = Player(row, True)
      print(player)
      print(player.get_rating())
      #find the players team
      if player.team not in teams:
        teams[player.team] = Team(player.team)

      teams[player.team].add_players(player)

  chosen_teams = [random.randint(0, len(teams) - 1) for _ in range(4)]
  chosen_teams = set(chosen_teams)
  if len(chosen_teams) != 4:
    while len(chosen_teams) != 4:
      chosen_teams.add(random.randint(0, len(teams) - 1))
  json = []
  diff = 1
  for i, item in enumerate(list(teams.items())):
    if i in chosen_teams:
      team = teams[item[0]]
      chosen = team.get_players(diff)
      print('Team : {0} Chosen: {1}'.format(team.name, chosen))
      json.append({
        'difficulty': diff,
        'category' : team.name,
        'items' : [player.name for player in chosen]
      })
      diff += 1
  print('[', end='')
  for i, team in enumerate(json):
    print('{{ "difficulty": {0}, "category": \"{1}\", "items": ['.format(team['difficulty'], team['category']), end='')
    for j, player in enumerate(team['items']):
      print("\"{0}\"".format(player), end='')
      if j != len(team['items']) - 1:
        print(',', end='')
    print(']}', end='')
    if i != len(json) - 1:
      print(',', end='')
  print(']')







  
