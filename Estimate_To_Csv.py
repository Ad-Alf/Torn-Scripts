import requests
import time

###############
#    Fixed    #
#   Variables #
###############
ranks = {
	"Absolute beginner": 1,
	"Beginner": 2,
	"Inexperienced": 3,
	"Rookie": 4,
	"Novice": 5,
	"Below average": 6,
	"Average": 7,
	"Reasonable": 8,
	"Above average": 9,
	"Competent": 10,
	"Highly competent": 11,
	"Veteran": 12,
	"Distinguished": 13,
	"Highly distinguished": 14,
	"Professional": 15,
	"Star": 16,
	"Master": 17,
	"Outstanding": 18,
	"Celebrity": 19,
	"Supreme": 20,
	"Idolized": 21,
	"Champion": 22,
	"Heroic": 23,
	"Legendary": 24,
	"Elite": 25,
	"Invincible": 26,
}

triggerLevel = (2, 6, 11, 26, 31, 50, 71, 100)
triggerCrime = (100, 5000, 10000, 20000, 30000, 50000)
triggerNetworth = (5000000, 50000000, 500000000, 5000000000, 50000000000)
estimatedStats = ("under 2k", "2k - 25k", "20k - 250k", "200k - 2.5m", "2m - 25m", "20m - 250m", "over 200m",)
    
###############
#  Functions  #
###############    
def fileWriter(name, string):
    with open(name + '.csv', 'a') as f:
        f.write(f'{string}\n')
                  
def ApiCall(type, id, key, selections = ''):
    r = requests.get('https://api.torn.com/' + type + '/' + id + '?selections=' + selections + '&key=' + key)
    return r.json()
     
def getFactionInfo(id, key):
    factionInfo = ApiCall('faction', id, key)
    return factionInfo   
    
def getMemberInfo(id, key):
    memberInfo = ApiCall('user', id, key, 'profile,personalstats,crimes')
    name = memberInfo['name']
    level = memberInfo['level']
    rankSplit = memberInfo['rank'].split(' ')
    rankString = rankSplit[0]
    if rankSplit[1].islower():
        rankString = rankString + ' ' + rankSplit[1]
    rank = ranks[rankString]
    crimes = memberInfo['criminalrecord']['total']
    networth = memberInfo['personalstats']['networth']
    xan = memberInfo['personalstats']['xantaken']
    awards = memberInfo['awards']
    age = memberInfo['age']
    
    print(f'Processing {name}')
        
    trLevel = 0
    trCrimes = 0
    trNetworth = 0 
    
    for x in triggerLevel:
        if x <= level:
            trLevel +=1
              
          
    for x in triggerCrime:
        if x <= crimes:
            trCrimes +=1 
    
    for x in triggerNetworth:
        if x <= networth:
            trNetworth +=1
   
    statLevel = rank - trLevel - trCrimes - trNetworth - 1
    try:
        estimate = estimatedStats[statLevel]
    except IndexError:
        estimate = 'N/A'
    fileWriter(factionName, f'{name}, {level}, {rank}, {estimate}, {xan}, {awards}, {age}') 
    
    return

###############
#     App     #
###############

#Variables
factionID = input('Enter faction ID: ')
apiKey = input('Enter API key: ')
factionInfo = getFactionInfo(factionID, apiKey)
factionName = factionInfo['name'] 

#Execute program
print(f'Gathering data for {factionName}')
fileWriter(factionName, 'Name, Level, Rank, Stats, Xan, Awards, Age')
for key in factionInfo['members']:
    getMemberInfo(key, apiKey)
    time.sleep(0.75)