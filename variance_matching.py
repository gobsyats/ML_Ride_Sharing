import statistics
import constants
from datetime import datetime
from dbconnection import db

def variance_regression(userid):
    #ridercollection = db.ridersndrivers
    for j in range(len(userid)):
        chat = []
        safe = []
        punctual = []
        comfort = []
        friend = []
        feedbackCollection = db.feedbackCollection
        cursor = feedbackCollection.find({"user_who_is_rating_id": userid[j]})
        riderFdBack = list(cursor)
        #print(len(riderFdBack))
        for i in range(len(riderFdBack)):
            chat.append(riderFdBack[i][constants.CHAT_RATE])
            safe.append(riderFdBack[i][constants.SAFE_RATE])
            punctual.append(riderFdBack[i][constants.PUNCTUAL_RATE])
            friend.append(riderFdBack[i][constants.FRIENDLINESS_RATE])
            comfort.append(riderFdBack[i][constants.COMFORT_RATE])
        #print("chat", chat)
        #print("safe", safe)
        #print("punctual", punctual)
        #print("friend", friend)
        #print("comfort", comfort)
        datalist = {
             constants.CHATTY_SCORE: statistics.variance(chat),
             constants.SAFETY_SCORE: statistics.variance(safe),
             constants.PUNCTUALITY_SCORE: statistics.variance(punctual),
             constants.FRIENDLINESS_SCORE: statistics.variance(friend),
             constants.COMFORTIBILITY_SCORE: statistics.variance(comfort)
             }
        print(datalist)
        max_score = round(max(datalist.values()), 2)
        max_key = max(datalist, key=datalist.get)

        print(max_score, max_key)
        ridercollection = db.ridersndrivers
        print("-------------------")
    return constants.EMPTY_STRING

userIdList = [6995, 52160, 91332, 101447]
variance_regression(userIdList)
