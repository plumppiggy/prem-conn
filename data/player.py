import random
import functools

TEAMS = {'Man City' : 5, 'Liverpool' : 5, 'Spurs' : 5, 'Arsenal' : 5, 'Brighton' : 3, 'West Ham' : 4, 'Aston Villa' : 3, 'Nottm Forest' : 2, 
         'Crystal Palace' : 3, 'Fulham' : 1, 'Brentford': 1, 'Newcastle' : 3, 'Man Utd': 5, 'Chelsea' : 5, 'Bournemouth': 3, 'Wolves': 3,
         'Sheffield Utd': 1, 'Everton': 3, 'Burnley': 2, 'Luton': 1}
DIFFMAP = {1 : 0.1, 2 : 0.01, 3: 0.02, 4: 0.001}


class Player:

  def __init__(self, row, is_reading = False):
    if not is_reading:
      col = row.find_all('td')
    else:
      col = row
    self.name = col[0]
    self.position = col[1]
    self.team = col[2]
    self.price = col[3]
    self.total_points = col[4]

    if not is_reading:
      self.name = self.name.text
      self.team = self.team.text
      self.position = self.position.text
      self.price = self.price.text
      self.total_points = self.total_points.text

  def __str__(self) -> str:
    return self.name + ' ' + self.team + ' ' + self.position + ' ' + self.price + ' ' + self.total_points
  
  def get_info(self):
    info = [self.name, self.position, self.team, self.price, self.total_points]
    return info
  
  # Returns a value indicating how 'known' this person is
  def get_rating(self):
    score = TEAMS[self.team]
    if self.total_points == 0:
      # then they haven't played
      score /= 2
    
    score *= float(self.total_points)
    score *= float(self.price)
    return score
  
def get_headers():
  return ["Name", "Position", "Team", "Price", "Total Points"]

def get_score_wrapper(sum, player):
  return sum + player.get_rating()

class Team:
  def __init__(self, name) -> None:
    self.players = []
    self.name = name

  def add_players(self, players):
    if isinstance(players, list):
      self.players.extend(players)
    else:
      if int(players.total_points) > 3:
        self.players.append(players)

  def get_total_points(self):
    return functools.reduce(lambda x, y: x + y.get_rating(), self.players, 0)


  def get_players(self, difficulty):
    chosen = {random.randint(0, len(self.players) - 1) for _ in range(3)}
    cur_players = set()
    total_points = functools.reduce(lambda x, y: x + y.get_rating(), self.players, 0)
    
    for idx in chosen:
      cur_players.add(self.players[idx])
    
    sm = functools.reduce(lambda x, y: x + y.get_rating(), cur_players, 0)
    while len(chosen) < 4 or sm / total_points < DIFFMAP[difficulty]:
      if (sm - DIFFMAP[difficulty]) > 0:
        min_score = max(cur_players, key=lambda x: x.get_rating())
      else:
        min_score = min(cur_players, key=lambda x: x.get_rating())
      new_chosen = set()
      new_players = set()
      for player, idx in zip(cur_players, chosen):
        if player != min_score and int(player.total_points) > 3:
          new_chosen.add(idx)
          new_players.add(player)
      chosen.clear()
      cur_players.clear()
      chosen, cur_players = new_chosen, new_players
      while len(cur_players) < 4:
        idx = random.randint(0, len(self.players) - 1)
        if idx not in chosen: 
          chosen.add(idx)
          cur_players.add(self.players[idx])
      sm = functools.reduce(lambda x, y: x + y.get_rating(), cur_players, 0)
    return cur_players
    