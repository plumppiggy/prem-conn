import requests
import pandas as pd

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
      history[i]['element'] = self.id
      history[i]['name'] = self.name
    return history

def rolling_average(df, window):
  return df.rolling(min_periods=1, window=window).mean().shift(1)

def get_player_averages(df):
  feature_names = []
  for stat in df[['total_points']]:
    print(stat)
    temp = df.groupby('element')[stat].apply(lambda x : rolling_average(x, 4))
    print(df.groupby('element')[stat].apply(lambda x : rolling_average(x, 4)))
    df['hello'] = temp.reset_index(level=0, drop=True)

  return df



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
    PLAYERS[new_player.id] = new_player.name
  
  player_df = None

  # Filter by MC players to reduce the number of players
  man_city_players = [player for player in players if 'Man City' == player.team]
  print(man_city_players)
  
  for player in man_city_players[:3]:
    if player_df is None:
      player_df = pd.DataFrame(player.get_player_history())
    else:
      history = player.get_player_history()
      for row in history:
        player_df.loc[len(player_df.index)] = row

  print(player_df)

  new_df = get_player_averages(player_df)

  print(new_df)



  #df = pd.DataFrame(players_json, columns=['first_name', 'team_code', 'strength_attack_away','expected_goals_per_90', 'expected_assists_per_90', 'points_per_game_rank', 'threat'])
  #print(df)

  
  
