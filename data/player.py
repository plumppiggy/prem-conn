import random

class Player:

  def __init__(self, row, is_reading = False):
    if not is_reading:
      col = row.find_all('td')
    else:
      col = row
    self.name = col[0]
    self.position = col[1]
    self.team = col[2]

    if not is_reading:
      self.name = self.name.text
      self.team = self.team.text
      self.position = self.position.text

  def __str__(self) -> str:
    return self.name + ' ' + self.team + ' ' + self.position
  
  def get_info(self):
    info = [self.name, self.position, self.team]
    return info
  
def GetHeaders():
  return ["Name", "Position", "Team"]


class Team:
  def __init__(self, name) -> None:
    self.players = []
    self.name = name

  def add_players(self, players):
    if type(players) == list:
      self.players.extend(players)
    else:
      self.players.append(players)

  def get_players(self):
    idx = random.randint(0, len(self.players) - 4)
    return self.players[idx:idx+4]