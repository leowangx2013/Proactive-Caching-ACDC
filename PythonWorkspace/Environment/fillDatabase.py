import pandas as pd
import mysql.connector
import string
import random
import pandas as pd
import numpy as np
from random import shuffle

db = mysql.connector.connect(user='root', password='socialsim', host='localhost',database='ACDCTestData')
cursor = db.cursor();

numberOfUniqueVideos = 500
numberOfUniqueClients = 300
simulationTime = 24*60*60 # one month

CategoryList = ['Music','MISC','News','Sports','Comedy']
subTypeDict = {'Music':['pop','rock','country'], \
				'News': ['political news','sports news','entertainment news'], \
				'Sports': ['basketball','baseball','football'], \
				'Comedy': ['FunnyAnimals','ComedyShow','Pranks'],\
				'MISC':['null','null','null']}

uniqueUserIdList = []
uniqueVideoIdList = []
videoCategoryTupleList = []


for i in range(0,numberOfUniqueClients): #
	uniqueUserIdList.append(''.join(random.choice(string.digits) for _ in range(6)))


## generate video ID
for i in range(0,numberOfUniqueVideos): # 10000
	uniqueVideoIdList.append(''.join(random.choice(string.digits) for _ in range(6)))

cat2videoID = dict()
for i in range(0,numberOfUniqueVideos): # 10000
	## flip to control category prob.
	num = np.random.choice(np.arange(0, 5), p = [0.3,0.3,0.1,0.2,0.1])
	videoCategoryTupleList.append((uniqueVideoIdList[i],CategoryList[num]))
	cat2videoID.setdefault(CategoryList[num],[]).append(uniqueVideoIdList[i])

## dictionary to save features
Table = {'row_names':[],'requestTime':[],'userId':[],'videoId':[],
		'sessionDuration':[],'avgChunkDuration':[],'chunks':[],'duration':[],
		'uploaded':[],'uploader':[],'category':[],'bitrate':[],'index':[], 'subtype':[]}

## 30 days
dailyRequest = []
subTypeProb = []
dailyCategoryProb = []

totalDays = 30
for d in range(totalDays):
	if 15 < d <= 18:
		## category prob. distribution
		pMusic = random.randint(25,30)/100.0
		pComedy = random.randint(5,10)/100.0
		pNews = random.randint(5,10)/100.0
		pSports = random.randint(30,40)/100.0
		pMISC = 1 - pMusic - pComedy - pNews - pSports
		dailyCategoryProb.append([pMusic,pMISC,pNews,pSports,pComedy])

		## daily # of request
		dailyRequest.append(random.randint(350,400))

		# subtype prob. distribution
		pSub1 = random.randint(50,55)/100.0
		pSub2 = random.randint(20,25)/100.0
		pSub3 = 1 - pSub1 - pSub2
		subTypeProb.append([pSub1,pSub2,pSub3])

	else:
		## category prob. distribution
		pMusic = random.randint(25,33)/100.0
		pComedy = random.randint(5,12)/100.0
		pNews = random.randint(5,10)/100.0
		pSports = random.randint(20,25)/100.0
		pMISC = 1 - pMusic - pComedy - pNews - pSports
		dailyCategoryProb.append([pMusic,pMISC,pNews,pSports,pComedy])

		## daily request
		dailyRequest.append(random.randint(200,250))

		## subtype prob. distribution
		pSub1 = random.randint(30,35)/100.0
		pSub2 = random.randint(30,35)/100.0
		pSub3 = 1 - pSub1 - pSub2
		subTypeProb.append([pSub1,pSub2,pSub3])

## hourly distribution for each category
def hour_distribution_fun(category):
	'''for each category '''
	hourlyDistribution = []
	if category == 'Sports':
		for h in range(24):
			if 19 <= h <= 23:
				hourlyDistribution.append(random.randint(8,12))
			else:
				hourlyDistribution.append(random.randint(4,6))
	elif category == 'News':
		for h in range(24):
			if 19 <= h <= 23 or 9 <= h < 12:
				hourlyDistribution.append(random.randint(6,10))
			else:
				hourlyDistribution.append(random.randint(2,4))
	elif category == 'Comedy':
		for h in range(24):
			if 12 <= h <= 15 or 19 <= h <= 22:
				hourlyDistribution.append(random.randint(5,8))
			else:
				hourlyDistribution.append(random.randint(2,4))
	elif category == 'Music':
		for h in range(24):
			if 19 <= h <= 23:
				hourlyDistribution.append(random.randint(8,12))
			else:
				hourlyDistribution.append(random.randint(2,5))
	else:
		hourlyDistribution = [1.0] * 24
	Distribution = 1.0*np.array(hourlyDistribution)/np.sum(hourlyDistribution)
	return Distribution

## daily distribution
for d in range(totalDays):
	## num of requests
	numberOfRequests = dailyRequest[d]
	subProb = subTypeProb[d]
	catProb = dailyCategoryProb[d]

	for i in range(1,numberOfRequests+1):
		category = CategoryList[np.random.choice(np.arange(0, 5), p = catProb)]
		videoId = random.choice(cat2videoID[category])

		## subtype
		subtypeList = subTypeDict[category]
		subtype = subtypeList[np.random.choice(np.arange(0, 3), p = subProb)]
		print(category)
		## sports(night), news(mornig and night), comedy(noon and night), music(night) daily distribution
		hourlyDistribution = hour_distribution_fun(category)
		hour = np.random.choice(np.arange(0,24), p = hourlyDistribution)
		realTime = simulationTime/24.0*hour + random.randint(60*1,60*59)
		
		## create a table
		Table['requestTime'].append(1480550400.0 + simulationTime*d + realTime)
		Table['row_names'].append(1)
		Table['userId'].append(uniqueUserIdList[random.randint(0,len(uniqueUserIdList)-1)])
		Table['videoId'].append(videoId)
		Table['sessionDuration'].append(random.randint(7,255))
		Table['avgChunkDuration'].append(1)
		Table['chunks'].append(1)
		Table['duration'].append(1)
		Table['uploaded'].append('null')
		Table['uploader'].append('null')
		Table['category'].append(category)
		Table['bitrate'].append(random.randint(7,255))
		Table['index'].append(i)
		Table['subtype'].append(subtype)


## convert to pandas table
df = pd.DataFrame(Table)
print(df.head())

try:
    deleteStatement = """DELETE FROM 'ACDCTestData'.'YouTubeDataset';""";
    cursor.execute(deleteStatement);
    db.commit();
except:
    db.rollback();

## commit database
for index, row in df.iterrows():
	try:
		executeStatement = """INSERT INTO `ACDCTestData`.`YouTubeDataset` 
			(`row_names`, `requestTime`, `userId`, `videoId`, 
			`sessionDuration`, `avgChunkDuration`, `chunks`, `duration`, 
			`uploaded`, `uploader`, `category`, `bitrate`, `index`,`subtype`)
			VALUES ('"""+str(row['row_names'])+"""', '"""+str(row['requestTime'])+"""', '"""+str(row['userId'])+"""',
			'"""+str(row['videoId'])+"""', '"""+str(row['sessionDuration'])+"""', '"""+str(row['avgChunkDuration'])+"""',
			'"""+str(row['chunks'])+"""', '"""+str(row['duration'])+"""', '"""+str(row['uploaded'])+"""', '"""+str(row['uploader'])+"""',
			'"""+str(row['category'])+"""', '"""+str(row['bitrate'])+"""', '"""+str(row['index'])+"""', '"""+str(row['subtype'])+"""');"""
	        # print (executeStatement)
                cursor.execute(executeStatement);
		db.commit();
	except:
		db.rollback();
db.close();

print("well done")




