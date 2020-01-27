from dbconnection import db
import constants
import commons

def feedback_aggr(userQ):
    for i in range(0, len(userQ)):
        rate_chat_total = 0
        rate_safe_total = 0
        rate_punctual_total = 0
        rate_friend_total = 0
        rate_comfort_total = 0
        feedbackCollection = db.feedbackCollection
        cursor = feedbackCollection.find({"user_who_is_rating_id": userQ[i]})
        riderFdBack = list(cursor)
        #print(riderFdBack)
        for j in range(0, len(riderFdBack)):
            #print(riderFdBack[j])
            #print(riderFdBack[j][constants.CHAT_RATE], riderFdBack[j][constants.SAFE_RATE],
             #     riderFdBack[j][constants.PUNCTUAL_RATE], riderFdBack[j][constants.FRIENDLINESS_RATE], riderFdBack[j][constants.COMFORT_RATE])
            rate_chat_total += riderFdBack[j][constants.CHAT_RATE]
            rate_safe_total += riderFdBack[j][constants.SAFE_RATE]
            rate_punctual_total += riderFdBack[j][constants.PUNCTUAL_RATE]
            rate_friend_total += riderFdBack[j][constants.FRIENDLINESS_RATE]
            rate_comfort_total += riderFdBack[j][constants.COMFORT_RATE]
        aggr_rating = [rate_chat_total, rate_safe_total, rate_punctual_total, rate_friend_total, rate_comfort_total]
        print(aggr_rating)