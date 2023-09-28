import csv
import random
import sys
import pandas as pd
from player import Team
from player import Player
from player import TEAMS


# Maps the player stat the the game grouping
PLAYER_PROPERTIES = {'penalties_saved' : 'Players who saved a penatly', 'penalties_missed' : 'Players who missed a penalty',
                      'goals_scored' : 'Players who have scored',  'own_goals': 'Players who have scored an own goal', 
                      'red_cards' : 'Players who have gotten a red card', 'clean_sheets': 'Players that have kept a clean sheet' }

def define_game(json):
  '''
  Print and format the created game in a way that is consistent with the TypeScript Group[] Type
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
  '''
  Create games based on players that have a team in common
  '''
  teams = {}
  # Read the data from the csv
  with open('playerdata.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
      # Convert the row to a player
      player = Player(row, True)
      # Find the players team
      if player.team not in teams:
        teams[player.team] = Team(player.team)
      teams[player.team].add_players(player)

  # Pick the teams to use
  chosen_teams = {random.randint(0, len(teams) - 1) for _ in range(3)}

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

  json = []
  diff = 1
  for i, item in enumerate(list(teams.items())):
    if i in chosen_teams:
      team = teams[item[0]]
      chosen = team.get_players(diff)
      json.append({
        'difficulty': diff,
        'category' : team.name,
        'items' : [player.name for player in chosen]
      })
      diff += 1

  #define_game(json)
  return json

class PlayerData:
  '''
  Holds the player data from csv's and parses the data
  '''
  def __init__(self):
    self.df = pd.read_csv('players.csv')
    self.goal_stats = pd.read_csv('GoalsScored.csv')

  def get_players_feature(self, field):
    '''
    Returns the players who have > 0 of the given field
    For example if the field is penalties saved the result is the players who have saved a pen
    '''
    results = self.df[self.df[field] > 0]['second_name']
    return results
  
  def get_hatricks(self):
    res = self.goal_stats[self.goal_stats.isin([3]).any(axis=1)]['name']
    print(res)

  def group_by_squad_number(self, number):
    '''
    TODO: Group players by number (shirt number)
    '''
    pass

  def parse_news(self):
    '''
    Read the 'news' column of the data to try and extract any interesting info
    '''
    on_loan = self.df[self.df['news'].str.contains('loan')==True]['second_name']
    injured = self.df[self.df['news'].str.contains('injury')==True]['second_name']

def get_random_categories(player_data):
  '''
  Get the groupings of players by the random categories
  '''
  json = []
  diff = 1

  # Go through the premade groups
  # TODO: Shuffle the list so it changes each time (right now only four have four players)
  for field, title in PLAYER_PROPERTIES.items():
    # Get the players that reach the field description
    res = player_data.get_players_feature(field)

    # Not enough players - don't add
    if len(res) < 4:
      continue

    res = [r for r in res]
    # Shuffle the results
    random.shuffle(res)

    # Format as a JSON
    json.append({
      'difficulty': diff,
      'category': title,
      'items': [r for r in res[:4]]
    })
    # Increase the difficulty
    diff += 1

  return json


if __name__ == '__main__':

  # DATA Storage (Basically)
  player_data = PlayerData()

  # Go through new source and get common factors
  # player_data.parse_news()

  # Not enough players have scored hatricks to implement this
  # hatrick_heros = player_data.get_hatricks()

  args = len(sys.argv)
  if args == 1:
    print('enter -help for a list of cmds')
  res = None

  for i in range(1, args):
    cmd = sys.argv[i]
    if cmd == '-teams':
      res = group_players_by_team()
    elif cmd == '-random':
      res = get_random_categories(player_data)
    elif cmd == '-help':
      print('Enter -teams for team based game or enter -random for a randomly made game')
    else:
      print('Unrecognized command')

  if res is not None:
    define_game(res)
