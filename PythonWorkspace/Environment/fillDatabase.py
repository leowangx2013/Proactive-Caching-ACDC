import pandas as pd
import mysql.connector
import string
import random
import pandas as pd
import numpy as np
from random import shuffle

db = mysql.connector.connect(user='root', password='socialsim', host='localhost',database='ACDCTestData')
cursor = db.cursor();


numberOfUniqueVideos = 200
numberOfUniqueClients = 300
simulationTime = 24*60*60 # one month
# numberOfRequests = 672

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

for i in range(0,numberOfUniqueVideos): # 200
	uniqueVideoIdList.append(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))

Table = {'row_names':[],'requestTime':[],'userId':[],'videoId':[],
		'sessionDuration':[],'avgChunkDuration':[],'chunks':[],'duration':[],
		'uploaded':[],'uploader':[],'category':[],'bitrate':[],'index':[], 'subtype':[]}

## 30 days
dailyRequest = []
subTypeProb = []
dailyCategoryProb = []

for d in range(30):
	if 15 < d <= 18:
		pMusic = random.randint(25,30)/100.0
		pComedy = random.randint(5,10)/100.0
		pNews = random.randint(5,10)/100.0
		pSports = random.randint(30,40)/100.0
		pMISC = 1 - pMusic - pComedy - pNews - pSports
		dailyCategoryProb.append([pMusic,pMISC,pNews,pSports,pComedy])

		## daily request
		dailyRequest.append(random.randint(70,80))

		# subtype prob. distribution
		pSub1 = random.randint(50,55)/100.0
		pSub2 = random.randint(20,25)/100.0
		pSub3 = 1 - pSub1 - pSub2
		subTypeProb.append([pSub1,pSub2,pSub3])

	else:
		pMusic = random.randint(25,33)/100.0
		pComedy = random.randint(5,12)/100.0
		pNews = random.randint(5,10)/100.0
		pSports = random.randint(20,25)/100.0
		pMISC = 1 - pMusic - pComedy - pNews - pSports
		dailyCategoryProb.append([pMusic,pMISC,pNews,pSports,pComedy])

		## daily request
		dailyRequest.append(random.randint(50,60))

		## subtype prob. distribution
		pSub1 = random.randint(30,35)/100.0
		pSub2 = random.randint(30,35)/100.0
		pSub3 = 1 - pSub1 - pSub2
		subTypeProb.append([pSub1,pSub2,pSub3])


## daily distribution
for d in range(30):
	prob = dailyCategoryProb[d]
	for i in range(0,numberOfUniqueVideos): # 200
		## flip to control category prob.
		num = np.random.choice(np.arange(0, 5), p = prob)
		videoCategoryTupleList.append((uniqueVideoIdList[i],CategoryList[num]))
	
	## # of requests
	numberOfRequests = dailyRequest[d]
	subProb = subTypeProb[d]

	for i in range(1,numberOfRequests+1):
		vidCatTuple = videoCategoryTupleList[random.randint(0,len(videoCategoryTupleList)-1)]
		videoId = vidCatTuple[0]
		category = vidCatTuple[1]
		subtypeList = subTypeDict[category]
		subtype = subtypeList[np.random.choice(np.arange(0, 3), p = subProb)]

		## create a table
		Table['row_names'].append(1)
		Table['requestTime'].append(1397426400.07611+ simulationTime*d + (simulationTime/numberOfRequests)*(i-1))
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
	        print (executeStatement)
                cursor.execute(executeStatement);
		db.commit();
	except:
		db.rollback();
db.close();

print("well done")




