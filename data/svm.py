from sklearn import svm
# support vector machine
# Learning
# x = [[0,0], [1,1]]
# y = [0, 1]
# clf = svm.SVC()
# clf.fit(x, y)

# print(clf.predict([[2., 2.]]))

# x = [[team_h, team_a]]
# y = [win, loss]  1 is win, 0 is loss
RESULTS = {0: 'loss', 1: 'win', 2: 'draw'}
# predict  game: [team_h, team_a]
# The values in this dict need to be unique to the team
TEAM_RATINGS = {'Man City' : 85.67, 'Liverpool': 84, 'Chelsea': 83, 'Spurs': 82, 'Arsenal': 81, 'Man Utd': 81.9, 'Luton': 69, 'West Ham': 78.8,
                'Newcastle': 79, 'Aston Villa': 78.9, 'Wolves': 78, 'Everton' : 77, 'Nottm Forest': 76.5, 'Crystal Palace': 76, 'Burnley' : 73,
                'Fulham': 75, 'Brighton': 75.7, 'Brentford': 74.9, 'Bournemouth': 74, 'Sheffield Utd': 72}

CITY = TEAM_RATINGS['Man City']
LIV = TEAM_RATINGS['Liverpool']
CHE = TEAM_RATINGS['Chelsea']
SPURS = TEAM_RATINGS['Spurs']
HAM = TEAM_RATINGS['West Ham']
ARS = TEAM_RATINGS['Arsenal']
UTD = TEAM_RATINGS['Man Utd']
LUTON = TEAM_RATINGS['Luton']
NEW = TEAM_RATINGS['Newcastle']
VILLA = TEAM_RATINGS['Aston Villa']
WOL = TEAM_RATINGS['Wolves']
EVE = TEAM_RATINGS['Everton']
NOTM = TEAM_RATINGS['Nottm Forest']
CRY = TEAM_RATINGS['Crystal Palace']
BUR = TEAM_RATINGS['Burnley']
FUL = TEAM_RATINGS['Fulham']
BRI = TEAM_RATINGS['Brighton']
BRE = TEAM_RATINGS['Brentford']
BOU = TEAM_RATINGS['Bournemouth']
SHE = TEAM_RATINGS['Sheffield Utd']

def predict_game (clf, hometeam, awayteam, actual='Unknown'):
    hometeam_name, awayteam_name = None, None

    for k, v in TEAM_RATINGS.items():
        if v == hometeam:
            hometeam_name = k
        if v == awayteam:
            awayteam_name = k

    res = clf.predict([[hometeam, awayteam]])[0]
    print(f"{hometeam_name} vs. {awayteam_name} \nPrediction: {RESULTS[res]} \nActual:     {actual}")

# 0 loss 1 win 2 draw
gameweek_1 = [[BUR, CITY], [ARS, NOTM], [BOU, HAM], [BRI, LUTON], [EVE, FUL], [SHE, CRY], [NEW, VILLA], [BRE, SPURS], [CHE, LIV], [UTD, WOL]]
gameweek_1_res = [0, 1, 2, 1, 0, 0, 1, 2, 2, 1]

clf = svm.SVC()
clf.fit(gameweek_1, gameweek_1_res)

print('Game Week 2 Predictions')
predict_game(clf, NOTM, SHE, RESULTS[1])

# More Gameweeks gameweek 2 is cummualtive of previous weeks
gameweek_2 = gameweek_1 + [[NOTM, SHE], [FUL, BRE], [LIV, BOU], [WOL, BRI], [SPURS, UTD], [CITY, NEW], [VILLA, EVE], [HAM, CHE], [CRY, ARS]]
gameweek_2_res = gameweek_1_res + [1, 0, 1, 0, 1, 1, 1, 1, 0]

clf = svm.SVC()
clf.fit(gameweek_2, gameweek_2_res)

print('Game Week 3 Predictions')

predict_game(clf, CHE, LUTON, RESULTS[1])

gameweek_3 = gameweek_2 + [[CHE, LUTON], [BOU, SPURS], [ARS, FUL], [BRE, CRY], [EVE, WOL], [UTD, NOTM], [BRI, HAM], [BUR, VILLA], [SHE, CITY], [NEW, LIV]]
gameweek_3_res = gameweek_2_res + [1, 0, 2, 2, 0, 1, 0, 0, 0, 0]

clf = svm.SVC()
clf.fit(gameweek_3, gameweek_3_res)

print('Game Week 4 Predictions')
predict_game(clf, LUTON, HAM, RESULTS[0]) # RES 0
predict_game(clf, BUR, SPURS, RESULTS[1]) # RES 0
predict_game(clf, LIV, VILLA, RESULTS[1]) # RES 1

gameweek_4 = gameweek_3 + [[LUTON, HAM], [SHE, EVE], [BRE, BOU], [BUR, SPURS], [CHE, NOTM], [CITY, FUL], [BRI, NEW], [CRY, WOL], [LIV, VILLA], [ARS, UTD]]
gameweek_4_res = gameweek_3_res + [0, 2, 2, 0, 0, 1, 1, 1, 1, 1]

clf = svm.SVC()
clf.fit(gameweek_4, gameweek_4_res)

print('Game Week 5 Predictions')
predict_game(clf, WOL, LIV, RESULTS[0]) # RES 0
predict_game(clf, VILLA, CRY, RESULTS[1]) # RES 1
predict_game(clf, FUL, LUTON, RESULTS[1]) # RES 1

gameweek_5 = gameweek_4 + [[WOL, LIV], [VILLA, CRY], [FUL, LUTON], [UTD, BRI], [SPURS, SHE], [HAM, CITY], [NEW, BRE], [BOU, CHE], [EVE, ARS], [NOTM, BUR]]
gameweek_5_res = gameweek_4_res + [0, 1, 1, 0, 1, 0, 1, 2, 0, 2]

clf = svm.SVC()
clf.fit(gameweek_5, gameweek_5_res)

print('Game Week 6 Predictions')
predict_game(clf, CRY, FUL, RESULTS[2]) # RES 2
predict_game(clf, CITY, WOL, RESULTS[1]) # RES 1
predict_game(clf, CHE, VILLA, RESULTS[0]) # RES 0

gameweek_6 = gameweek_5 + [[CRY, FUL], [LUTON, WOL], [CITY, NOTM], [BRE, EVE], [BUR, UTD], [ARS, SPURS], [BRI, BOU], [CHE, VILLA], [LIV, HAM], [SHE, NEW]]
gameweek_6_res = gameweek_5_res + [2, 2, 1, 0, 0, 2, 1, 0, 1, 0]

clf = svm.SVC()
clf.fit(gameweek_6, gameweek_6_res)

print('Game Week 7 Predictions')
predict_game(clf, VILLA, BRI) 
predict_game(clf, BOU, ARS)
predict_game(clf, EVE, LUTON) 
predict_game(clf, FUL, CHE) 