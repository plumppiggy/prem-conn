import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

TEAMS = {}
PLAYERS = {}

class Team:
  def __init__(self, row):
    self.name = row['name']
    self.id = row['id']
    self.code = row['code']
    self.strength_attack_away = row['strength_attack_away']
    self.strength_attack_home = row['strength_attack_home']

class Player:
  def __init__(self, row):
    self.name = row['web_name']
    self.first_name = row['first_name']
    self.id = row['id']
    self.expected_goals_per_90 = row['expected_goals_per_90']
    self.team = TEAMS[row['team_code']]

  def get_player_history(self):
    response = requests.get(f'https://fantasy.premierleague.com/api/element-summary/{self.id}/')
    results = response.json()
    history = results['history']
    for i, row in enumerate(history):
      history[i]['element'] = int(self.id)
      history[i]['name'] = self.name
    return history

# Data Collection
def get_teams(dest='teams.csv'):
  '''
  Get the most recent Team data from the FPL API and write it to teams.csv or other file if specified
  '''
  response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
  json = response.json()
  teams_json = json['teams']
  team_df = pd.DataFrame(teams_json)
  team_df.to_csv(dest)

def get_players(dest='players.csv'):
  '''
  Get the most recent player data from the FPL API and write it to players.csv or other file if specified
  '''
  response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
  json = response.json()
  players_json = json['elements']
  player_df = pd.DataFrame(players_json)
  player_df.to_csv(dest)

def get_man_city_players(players, player_df, read_from_csv=True):
  '''
  Get the most recent data from the FPL API for Man City players or get it from the csv file if specified
  TODO: Expand this function to work for any team.
  '''
  if read_from_csv == True:
    return pd.read_csv('man_city_players_history.csv')
  # Else manually get the data from the API (time consuming)
  man_city_players = [player for player in players if 'Man City' == player.team]
  
  for player in man_city_players:
    if player_df is None:
      player_df = pd.DataFrame(player.get_player_history())
    else:
      history = player.get_player_history()
      for row in history:
        player_df.loc[len(player_df.index)] = row

  player_df.to_csv('man_city_players_history.csv')
  return player_df

# Data Analysis
def rolling_average(df, window):
  return df.rolling(min_periods=1, window=window).mean().shift(1)

def get_player_averages(df, prev_weeks = 3):
  # rename some of the dataframe columns
  df.rename(columns = {'element' : 'player_id', 'total_points': 'points'}, inplace = True)

  # TO-DO: figure out how to add difficulty to the calculations
  #df['oponent_difficulty'] = DIFFMAP[df.opponent_team]

  df = df.set_index(['fixture'])
  df = df.groupby(['player_id']).rolling(prev_weeks).agg({'minutes':np.sum, 'bps': np.sum, 'influence':np.sum}).shift(0).fillna(0)
  #df = df[df.fixture>prev_weeks]
  #df = df[df.minutes > 0]
  print(df)
  # for stat in df[['total_points']]:
  #   print(stat)
  #   temp = df.groupby('element')[stat].apply(lambda x : rolling_average(x, 4))
  #   df['rolling_average_tp'] = temp.reset_index(level=0, drop=True)

  return df

def do_predictions():
  '''
  Isolated function for the prediction logic - not yet implemented.
  '''
  player_df = None
  # Filter by MC players to reduce the number of players
  player_df = get_man_city_players(players, player_df)
  print(player_df.columns)

  new_df = get_player_averages(player_df)

  # # Linear Regression between the expected and actual points
  # x_pos = player_df.columns.get_loc('threat')
  # y_pos = player_df.columns.get_loc('total_points')
  # x = player_df.iloc[:, x_pos].values.reshape(-1, 1)
  # y = player_df.iloc[:, y_pos].values.reshape(-1, 1)

  # for i, item in enumerate(x):
  #   x[i] = float(item)
  # for i, item in enumerate(y):
  #   y[i] = float(item)

  # linear_regressor = LinearRegression()
  # linear_regressor.fit(x, y)
  # y_pred = linear_regressor.predict(x)

  # plt.scatter(x, y)
  # plt.plot(x, y_pred, color='red')
  # plt.show()

if __name__ == '__main__':

  response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
  json = response.json()
  teams_json = json['teams']
  players_json = json['elements']
  teams = []
  players = []

  for team in teams_json:
    new_team = Team(team)
    teams.append(new_team)
    TEAMS[new_team.code] = new_team.name

  for player in players_json:
    new_player = Player(player)
    players.append(new_player)
    PLAYERS[new_player.id] = new_player
  

  
  
