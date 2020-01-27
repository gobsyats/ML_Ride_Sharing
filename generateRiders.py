#Simulation Code for registration
from datetime import datetime
import random
from dbconnection import db
import constants
import commons
import operator

#for userId in range(1, 100001):
#for userId in range(200001, 300001):
for userId in range(300001, 400001):
        ridersCollection = db.ridersndrivers
        chattyScore = random.randrange(1, 6)
        comfartabilityScore = random.randrange(1, 6)
        friendlinessScore = random.randrange(1, 6)
        punctualityScore = random.randrange(1, 6)
        safetyScore = random.randrange(1, 6)
        chattyScore = random.randrange(1, 6)

        charDict = {constants.CHATTY_SCORE: chattyScore,
                     constants.SAFETY_SCORE: safetyScore,
                     constants.PUNCTUALITY_SCORE: punctualityScore,
                     constants.FRIENDLINESS_SCORE: friendlinessScore,
                     constants.COMFORTIBILITY_SCORE: comfartabilityScore}
        reg_classifier = max(charDict, key=charDict.get)
        #reg_classifier = commons.get_classifier(chattyScore, safetyScore, punctualityScore, friendlinessScore, comfartabilityScore)
        utt = random.randrange(2, 7)
        utt = utt*5

        activeUser = ""
        activeUserStatus = random.random()
        if activeUserStatus > 0.7:
            activeUser = constants.NO
        else:
            activeUser = constants.YES

        broadcasting = ""
        broadcastingStatus = random.random()
        if broadcastingStatus > 0.7:
            broadcasting = constants.YES
        else:
            broadcasting = constants.NO
        sourceZone = random.randrange(1, 263)
        source = commons.generate_location(sourceZone)

        #Rider Document
        riders = {constants.USER_ID: userId,
                    constants.CHAR_DICT: charDict,
                    constants.CHATTY_SCORE: chattyScore,
                    constants.SAFETY_SCORE: safetyScore,
                    constants.PUNCTUALITY_SCORE: punctualityScore,
                    constants.FRIENDLINESS_SCORE: friendlinessScore,
                    constants.COMFORTIBILITY_SCORE: comfartabilityScore,
                    constants.REG_CLASSIFIER: reg_classifier,
                    constants.ALSO_DRIVER: constants.NO,
                    constants.UTT: utt,
                    constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
                    constants.ACTIVE_STATE: constants.NO,
                    constants.CURRENT_ZONE: sourceZone,
                    constants.CURRENT_LOCATION: source,
                    constants.BROADCASTING: broadcasting,
                    constants.FEEDBACK_GIVEN: constants.NO,
                    constants.FEEDBACK_GOT_CHAT: 0,
                    constants.FEEDBACK_GOT_SAFE: 0,
                    constants.FEEDBACK_GOT_PUNCTUAL: 0,
                    constants.FEEDBACK_GOT_FRIEND: 0,
                    constants.FEEDBACK_GOT_COMFORT: 0,
                    constants.RATINGS_GOT_DICT: {},
                    constants.GOT_FEEDBACK_CLASSIFIER: constants.EMPTY_STRING,
                    constants.GIVEN_RATING_CHAT: 0,
                    constants.GIVEN_RATING_SAFE: 0,
                    constants.GIVEN_RATING_PUNCTUAL: 0,
                    constants.GIVEN_RATING_FRIEND: 0,
                    constants.GIVEN_RATING_COMFORT: 0,
                    constants.VARIANCE_DICT: {},
                    constants.GIVEN_FEEDBACK_CLASSIFIER: constants.EMPTY_STRING,

                  }
        rider_ids = ridersCollection.insert_one(riders)

count = ridersCollection.count_documents({})

print('Found ', count, 'records')