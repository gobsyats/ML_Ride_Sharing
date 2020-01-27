from dbconnection import db
import constants
import commons

def feedback_aggr_given(userQ):
      for i in range(0, len(userQ)):
        rate_chat_given_total = 0
        rate_safe_given_total = 0
        rate_punctual_given_total = 0
        rate_friend_given_total = 0
        rate_comfort_given_total = 0
        feedbackCollection_given = db.feedbackCollection
        cursor_given = feedbackCollection_given.find({"user_who_is_rating_id": userQ[i]})
        riderFdBack_given = list(cursor_given)
        #print(riderFdBack)
        for j in range(0, len(riderFdBack_given)):
            #print(riderFdBack[j])
            #print(riderFdBack[j][constants.CHAT_RATE], riderFdBack[j][constants.SAFE_RATE],
             #     riderFdBack[j][constants.PUNCTUAL_RATE], riderFdBack[j][constants.FRIENDLINESS_RATE], riderFdBack[j][constants.COMFORT_RATE])
            rate_chat_given_total += riderFdBack_given[j][constants.CHAT_RATE]
            rate_safe_given_total += riderFdBack_given[j][constants.SAFE_RATE]
            rate_punctual_given_total += riderFdBack_given[j][constants.PUNCTUAL_RATE]
            rate_friend_given_total += riderFdBack_given[j][constants.FRIENDLINESS_RATE]
            rate_comfort_given_total += riderFdBack_given[j][constants.COMFORT_RATE]
        aggr_rating_given = [rate_chat_given_total, rate_safe_given_total, rate_punctual_given_total, rate_friend_given_total, rate_comfort_given_total]
        #print(aggr_rating)
        feedback_classifier_given, regression_output = commons.get_classifier(rate_chat_given_total, rate_safe_given_total, rate_punctual_given_total, rate_friend_given_total, rate_comfort_given_total)
        #print(feedback_classifier)
        ridersndrivers = db.ridersndrivers
        ridersndrivers.find_one_and_update({constants.USER_ID: userQ[i]},
                                           {"$set": {constants.GIVEN_RATING_CHAT: rate_chat_given_total,
                                                     constants.GIVEN_RATING_SAFE: rate_safe_given_total,
                                                     constants.GIVEN_RATING_PUNCTUAL: rate_punctual_given_total,
                                                     constants.GIVEN_RATING_FRIEND: rate_friend_given_total,
                                                     constants.GIVEN_RATING_COMFORT: rate_comfort_given_total,
                                                     constants.GIVEN_FEEDBACK_CLASSIFIER: feedback_classifier_given,
                                                     constants.CLASSIFIER_CURRENT_OUTPUT: regression_output
                                                     }})