import constants
from dbconnection import db
import commons
import random
def basic_feedback(userMongoQ, driverMongoQ, userIdQ, driverId, tripId):
    feedback = {}
    userIdQ.append(driverId)
    userMongoQ.append(driverMongoQ)
    #print(userIdQ)
    user_count = len(userIdQ)
    feed_back_type = ""
    for i in range(user_count):
        for j in range(user_count):
            if i != j:

                ratingList = commons.getChar()
                chat = ratingList[0]
                safe = ratingList[1]
                punctual = ratingList[2]
                friend = ratingList[3]
                comfort = ratingList[4]
                feedback_given_classifier, classifier_to_int = commons.get_classifier(chat, safe, punctual, friend, comfort)

                avg_rating = (chat + safe + punctual + friend + comfort) / 5

                if j == user_count-1:
                    feed_back_type = "rider_to_driver"
                elif i == user_count-1:
                    feed_back_type = "driver_to_rider"
                else:
                    feed_back_type = "rider_to_rider"

                if feed_back_type == "rider_to_driver":
                    driving_rating = random.randrange(2, 5)
                    document = {
                        "feedback_type": feed_back_type,
                        "user_who_is_rating_Mongoid": userMongoQ[i],
                        "user_who_is_rating_id": userIdQ[i],
                        "user_getting_rated_Mongoid": userMongoQ[j],
                        "user_getting_rated_id": userIdQ[j],
                        "driver_rating": driving_rating,
                        constants.TRIP_ID: tripId,
                        constants.CHAT_RATE: chat,
                        constants.SAFE_RATE: safe,
                        constants.PUNCTUAL_RATE: punctual,
                        constants.FRIENDLINESS_RATE: friend,
                        constants.COMFORT_RATE: comfort,
                        "average_rating": avg_rating,
                        "feedback_given_classifier": feedback_given_classifier,
                        "feedback_given_classifier_to_int": classifier_to_int,
                        constants.TIME_STAMP: commons.getTimeStamp()
                    }
                else:

                    document = {
                        "feedback_type": feed_back_type,
                        "user_who_is_rating_Mongoid": userMongoQ[i],
                        "user_who_is_rating_id": userIdQ[i],
                        "user_getting_rated_Mongoid": userMongoQ[j],
                        "user_getting_rated_id": userIdQ[j],
                        constants.TRIP_ID: tripId,
                        constants.CHAT_RATE: chat,
                        constants.SAFE_RATE: safe,
                        constants.PUNCTUAL_RATE: punctual,
                        constants.FRIENDLINESS_RATE: friend,
                        constants.COMFORT_RATE: comfort,
                        "average_rating": avg_rating,
                        "feedback_given_classifier": feedback_given_classifier,
                        "feedback_given_classifier_to_int": classifier_to_int,
                        constants.TIME_STAMP: commons.getTimeStamp()
                    }
                #print(document)
                #print("")
                feedbackCollection = db.feedbackCollection
                feed_back_id = feedbackCollection.insert_one(document)
