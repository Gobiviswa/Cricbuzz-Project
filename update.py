from pycricbuzz import Cricbuzz
import pymongo
import json
import time

#getting cricbuzz api object
def getCbObject():
	cb = Cricbuzz()
	return cb

#getting mongodb object
def getMongoObject():
    mongo = pymongo.MongoClient()
    return mongo


#get all the available matches
def getMatches(cb):
	matches = cb.matches()
	return matches


#filtering matches as preview, progress and completed
def filterMatches(matches):
	preview , inprogress , complete = [] , [] , []
	for match in matches:
		
		state = match['mchstate']
		if state == "preview" or state == "delay":
			preview.append(match)
		elif state == "inprogress" or state == "stump" or state == "innings break" or state == "tea" or state == "lunch" or state == "rain":
			inprogress.append(Cricbuzz().scorecard(match['id']))
		else:
			complete.append(match)

	return preview, inprogress, complete

#clearing all the collections in DB before adding new data into it
def clearDB(mongo):
	mongo.cricbuzz.preview.delete_many({})
	mongo.cricbuzz.inprogress.delete_many({})
	mongo.cricbuzz.complete.delete_many({})

#inserting preview matches
def insertPreview(mongo, preview):
	db = mongo.cricbuzz.preview
	
	for match in preview:
		db.insert(match)


#inserting Live matches
def insertLive(mongo, inprogress):
	db = mongo.cricbuzz.inprogress
	
	for match in inprogress:
		db.insert(match)
		

#inserting completed matches
def insertComplete(mongo, complete):
	db = mongo.cricbuzz.complete	

	for match in complete:
		db.insert(match)
		
#checking data and sending to insert into DB			
def sendDB(matches):
	if matches != []:
		preview , inprogress , complete = filterMatches(matches)
		mongo = getMongoObject()
		clearDB(mongo)
		
		if preview == []:
			print("No Preview matches available to insert...")
		else:
			insertPreview(mongo, preview)
			print("preview matches data inserted")

		if inprogress == []:
			print("No Live matches available to insert...")
		else:
			insertLive(mongo, inprogress)
			print("live scorecard data inserted")

		if complete == []:
			print("No Completed matches available to insert...")
		else:
			insertComplete(mongo, complete)
			print("Completed matches inserted")
		


#getting Cricbuzz Object
cb = getCbObject()
while True:
	matches = getMatches(cb) #getting all the matches from CB
	sendDB(matches) #sending to DD
	time.sleep(10) #to make the function to run for every 10 seconds by which db will be updated continuously
