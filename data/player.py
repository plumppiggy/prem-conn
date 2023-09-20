class Player:

  def __init__(self, row):
    col = row.find_all('td')
    self.name = col[0].text
    self.team = col[1].text
    self.position = col[2].text

  def __str__(self) -> str:
    return self.name + ' ' + self.team + ' ' + self.position
  
  def get_info(self):
    info = [self.name, self.team, self.position]
    return info
  
def GetHeaders():
  return ["Name", "Team", "Position"]