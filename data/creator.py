from player import Player
from player import Team
import csv
import random
from player import create_map
from player import TEAMS
import pandas as pd


# Maps the player stat the the game grouping
PLAYER_PROPERTIES = {'penalties_saved' : 'Players who saved a penatly', 'penalties_scored' : 'Players who scored a penalty',
                      'goals_scored' : 'Players who have scored', 'own_goals' : 'Players who have scored an own goal'}




def define_game(json):
  '''
  Print and format the created game in a way that is consistent with the React App
  '''
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

def group_players_by_team():
  teams = {}
  # read the data from the csv
  with open('playerdata.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
      # covert the row to a player
      player = Player(row, True)
      #find the players team
      if player.team not in teams:
        teams[player.team] = Team(player.team)

      teams[player.team].add_players(player)

  for team, team_obj in teams.items():
    print(team)
    print(team_obj.get_total_points())

  # Pick the teams to use
  chosen_teams = {random.randint(0, len(teams) - 1) for _ in range(3)}

  print(chosen_teams)
  while len(chosen_teams) != 4:
    chosen_teams.add(random.randint(0, len(teams) - 1))
    new_teams = set()
    for i, idx in enumerate(chosen_teams):
      # let the difficulty be i
      if TEAMS[list(teams.keys())[idx]] < i + 1:
        # don't add the team
        pass
      else:
        new_teams.add(idx)
    chosen_teams = new_teams

  print(chosen_teams)
  for i in chosen_teams:
    print(list(teams.keys())[i])

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

  define_game(json)

class PlayerData:
  def __init__(self):
    self.df = pd.read_csv('players.csv')

  def get_players_feature(self, field):
    '''
    Returns the players who have > 0 of the given field
    For example if the field is penalties saved the result is the players who have saved a pen
    '''
    results = self.df[self.df[field] > 0]['second_name']
    return results


if __name__ == '__main__':
  player_data = PlayerData()

  pens_saved = player_data.get_players_feature('penalties_saved')
  print(pens_saved)

  scored = player_data.get_players_feature('goals_scored')
  print(scored)


  


  







  
