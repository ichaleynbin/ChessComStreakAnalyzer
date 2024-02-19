import urllib.request as getURL
from urllib.error import HTTPError
import json
from pprint import pprint as pp
import matplotlib.pyplot as plt

playerName = 'PatrickDaly'
startMonth = 1
startYear = 2022
startNumber = startYear*12+startMonth
endMonth = 6
endYear = 2023
endNumber = endYear*12+endMonth
controlVar = 'time_control'
controlVal = '600'

games = []
getMonth = startMonth
getYear = startYear
allArchives = json.loads(getURL.urlopen(f"https://api.chess.com/pub/player/{playerName}/games/archives").read())['archives']

print (allArchives)
checkArchives = [x for x in allArchives if startNumber <= (int(x.split("/")[-2])*12 + int(x.split("/")[-1])) <= endNumber]
print (checkArchives)
for archive in checkArchives:
    theseGames = json.loads(getURL.urlopen(archive).read())['games']
    games += [x for x in theseGames if x[controlVar] == controlVal]
print(len(games))
games.sort(key=lambda x: x['end_time'])
record = []
for game in games:
    white = game['white']
    black = game['black']
    if ((white['username']==playerName and white['result']=='win') or 
        (black['username']== playerName and black['result']=='win')):
        record.append(1)
    elif white['result'] in ['repetition','agreed','stalemate','insufficient']:
        #pp(game)
        record.append(0.5)
    else:   
        record.append(0)
        
wStreaks,lStreaks = [],[]
curWStreak, curLStreak = 0,0
for result in record:
    if curWStreak > 0:
        if result == 1:
            curWStreak+=1
        elif curWStreak > 0:
            wStreaks.append(min(10,curWStreak))
            curWStreak = 0
            if result == 0:
                curLStreak = 1
    elif curLStreak > 0:
        if result == 0:
            curLStreak += 1
        elif curLStreak > 0:
            lStreaks.append(min(10,curLStreak))
            curLStreak = 0
            if result == 1:
                curWStreak = 1
    else:
        if result == 1:
            curWStreak = 1
        elif result == 0:
            curLStreak = 1
if curLStreak>0:
    lStreaks.append(min(10,curLStreak))
elif curWStreak > 0:
    wStreaks.append(min(10,curWStreak))

print(lStreaks)
plt.hist(lStreaks,bins=min(max(lStreaks),10))
plt.xlabel("Streak Length")
plt.ylabel("Number of Streaks")
plt.title(f"Loss Streaks, 10 minute games, beginning {startMonth}/{startYear} ending {endMonth}/{endYear}")
plt.show()
print(wStreaks)
plt.hist(wStreaks,bins=min(max(lStreaks),10))
plt.xlabel("Streak Length")
plt.ylabel("Number of Streaks")
plt.title(f"Win Streaks, 10 minute games, beginning {startMonth}/{startYear} ending {endMonth}/{endYear}")
plt.show()