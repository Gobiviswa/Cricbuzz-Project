from flask import Flask , render_template
import pymongo 
import json

application = Flask(__name__)

#getting MongoDB object
def getMongoObject():
	client = pymongo.MongoClient('localhost:27017')
	return client

#routing for the main page
@application.route('/')
def main():
	return render_template("index.html");


#getting preview data from db
@application.route('/getPreviewData',methods=['POST'])
def getPreviewData():
	try:
		mongo = getMongoObject();
		previewData = mongo.cricbuzz.preview.find()
		matchList = []
		number = 0

		if previewData.count() == 0:
			matchList = []
		else:	
			for match in previewData:
				number = number+1
				matchData = {
					"MatchNumber" : match['mnum'],
					"Description"  : match['mchdesc'],
					"Result"       : match['status'],
					"MatchType"   : match['type'],
					"Series"       : match['srs'],
					"MatchNo"   : number,
				}
				matchList.append(matchData);
	
	except Exception as e:
		return str(e)

	return json.dumps(matchList)


#getting Live scorecard from db
@application.route('/getLiveData',methods=['POST'])
def getLiveData():
	try:
		mongo = getMongoObject();
		scorecard = mongo.cricbuzz.inprogress.find()
		matchList = []
		number = 0

		if scorecard.count() == 0:
			matchList = []
		else:	
			for score in scorecard:
				number = number+1
				matchData = {
					'matchdesc' : score['matchinfo']['mchdesc'],
				  'matchnumber' : score['matchinfo']['mnum'],
					"totalruns" : score['scorecard'][0]['runs'],
					"overs"     : getOvers(score['scorecard'][0]['bowlcard']) ,
					"wickets"   : score['scorecard'][0]['wickets'],
					"bowlteam"  : score['scorecard'][0]['bowlteam'],
					"batteam"   : score['scorecard'][0]['batteam'],
					"runrate"   : score['scorecard'][0]['runrate'],
					"bowlcard"  : score['scorecard'][0]['bowlcard'], #array of bowling details
					"batcard"   : score['scorecard'][0]['batcard'], #array of batting details
					"status"    : score['matchinfo']['status'],
					"series"    : score['matchinfo']['srs'],
				    "bowlteamimg" : getTeamImg(score['scorecard'][0]['bowlteam']),
				    "batteamimg": getTeamImg(score['scorecard'][0]['batteam']),
				    "number"    : number,
				}
				
				matchList.append(matchData);
	except Exception as e:
		return str(e)

	return json.dumps(matchList)		


#getting completed data from db
@application.route('/getCompletedData',methods=['POST'])
def getCompletedData():
	try:
		mongo = getMongoObject();
		resultData = mongo.cricbuzz.complete.find()
		
		matchList = []
		number = 0

		if resultData.count() == 0:
			matchList = []
		else:	
			for match in resultData:
				number = number + 1
				matchData = {
					"MatchNumber" : match['mnum'],
					"Description"  : match['mchdesc'],
					"Result"       : match['status'],
					"MatchType"   : match['type'],
					"Series"       : match['srs'],
					"MatchNo"      : number,
				}
				matchList.append(matchData);


	except Exception as e:
		return str(e)

	return json.dumps(matchList)


#for getting team image
def getTeamImg( teamName ):
	mongo = getMongoObject();
	teamImages = mongo.cricbuzz.teamImages.find()
	imageUrl = ""

	for imagedic in teamImages:
		if teamName in imagedic.keys():
			imageUrl = imagedic[teamName]

	return imageUrl		

#to get over count in float
def getOvers(bowlcard):
	overs = 0
	for bowlcarddic in bowlcard:
		overs = overs + float(bowlcarddic['overs'])

	return overs;	
	

	
if __name__ == '__main__':
	application.run()	