import statistics
import constants
from datetime import datetime
from dbconnection import db


#Giving Classifier
def variance_given_classifier(userid):
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
        #print("Feedback given by User:", userid[j], "to User" userid)
        #print("chatty rating", chat)
        #print("safety rating", safe)
        #print("punctuality rating", punctual)
        #print("friendliness rating", friend)
        #print("comfortability rating", comfort)
        chat_var = statistics.variance(chat)
        safe_var = statistics.variance(safe)
        punctual_var = statistics.variance(punctual)
        friend_var = statistics.variance(friend)
        comfort_var = statistics.variance(comfort)

        chat_variance = round(chat_var, 2)
        safe_variance = round(safe_var, 2)
        punctual_variance = round(punctual_var, 2)
        friend_variance = round(friend_var, 2)
        comfort_variance = round(comfort_var, 2)

        if chat_variance == 0.0 or chat_variance == 0:
             chat_variance = 0.1
        elif safe_variance == 0.0 or safe_variance == 0:
             safe_variance = 0.1
        elif punctual_variance == 0.0 or punctual_variance == 0:
             punctual_variance = 0.1
        elif friend_variance == 0.0 or friend_variance == 0:
             friend_variance = 0.1
        elif comfort_variance == 0.0 or comfort_variance == 0:
             comfort_variance = 0.1

        datalist = {
             constants.CHATTY_SCORE: chat_variance,
             constants.SAFETY_SCORE: safe_variance,
             constants.PUNCTUALITY_SCORE: punctual_variance,
             constants.FRIENDLINESS_SCORE: friend_variance,
             constants.COMFORTIBILITY_SCORE: comfort_variance
             }
        max_score = round(max(datalist.values()), 2)
        max_key = max(datalist, key=datalist.get)
        #print(datalist)
        #print(max_score)
        #print(max_key)

        ridersndrivers = db.ridersndrivers
        ridersndrivers.find_one_and_update({constants.USER_ID: userid[j]},
                                           {"$set":{constants.GIVEN_RATING_CHAT: chat,
                                                    constants.GIVEN_RATING_SAFE: safe,
                                                    constants.GIVEN_RATING_PUNCTUAL: punctual,
                                                    constants.GIVEN_RATING_FRIEND: friend,
                                                    constants.GIVEN_RATING_COMFORT: comfort,
                                                     constants.VARIANCE_DICT: datalist,
                                                     constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                                                     }})
        cursor = ridersndrivers.find({constants.USER_ID: userid[j]})
        list_data = list(cursor)
        given_fdbk_classifier_int = 0
        if max_key == constants.CHATTY_SCORE:
            given_fdbk_classifier_int = 1
        elif max_key == constants.SAFETY_SCORE:
            given_fdbk_classifier_int = 2
        elif max_key == constants.PUNCTUALITY_SCORE:
            given_fdbk_classifier_int = 3
        elif max_key == constants.FRIENDLINESS_SCORE:
            given_fdbk_classifier_int = 4
        elif max_key == constants.COMFORTIBILITY_SCORE:
            given_fdbk_classifier_int = 5

        give_fdbck_data = db.Give_Fdbck_Train
        cursor_check = give_fdbck_data.find({constants.USER_ID:userid[j]})
        check_list = list(cursor_check)
        #print(check_list)
        if check_list == [] or check_list == constants.EMPTY_STRING or check_list == None:
            train_fdbck_givendocument = {
                constants.USER_ID: list_data[0][constants.USER_ID],
                constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                constants.VARIANCE_DICT: datalist,
                constants.UTT: list_data[0][constants.UTT],
                "max_variance": max_score,
                constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                constants.GIVEN_FEEDBACK_CLASSIFIER_INT: given_fdbk_classifier_int,
                constants.TIME_STAMP: datetime.now()
            }

            give_fdbck_id = give_fdbck_data.insert_one(train_fdbck_givendocument)
        else:
            give_fdbck_data.find_one_and_update({constants.USER_ID: userid[j]},
                                            {"$set":    {constants.USER_ID: list_data[0][constants.USER_ID],
                                                         constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                                                         constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                                                         constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                                                         constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                                                         constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                                                         constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                                                         constants.VARIANCE_DICT: datalist,
                                                         constants.UTT: list_data[0][constants.UTT],
                                                         "max_variance": max_score,
                                                         constants.GIVEN_FEEDBACK_CLASSIFIER: max_key,
                                                         constants.GIVEN_FEEDBACK_CLASSIFIER_INT: given_fdbk_classifier_int,
                                                         constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)
                                                      }})

    return constants.EMPTY_STRING


#Got Classifier
def variance_got_classifier(userid):
    #ridercollection = db.ridersndrivers
    for j in range(len(userid)):
        rated_chat = 0
        rated_safe = 0
        rated_punctual = 0
        rated_friend = 0
        rated_comfort = 0
        #print("Rating for User ", userid[j])
        feedbackCollection = db.feedbackCollection
        cursor = feedbackCollection.find({"user_getting_rated_id": userid[j]})
        dataList = list(cursor)
        for i in range(0, len(dataList)):
            if dataList[i] == {} or dataList[i] == None:
                ""
                #print("Found Empty Rider")
            else:
                user_rating_the_rider = dataList[i]["user_who_is_rating_id"]
                if user_rating_the_rider == "" or user_rating_the_rider == None:
                    ""
                    #print("Actually Found Empty Rider")
                else:
                    riders = db.ridersndrivers
                    rider_cursor = riders.find({constants.USER_ID: user_rating_the_rider})
                    rider_data_list = list(rider_cursor)
                    variance_dict = rider_data_list[0][constants.VARIANCE_DICT]
                    #print(dataList[i])
                    #print("Rating=", dataList[i][constants.CHAT_RATE], dataList[i][constants.SAFE_RATE], dataList[i][constants.PUNCTUAL_RATE],
                     #     dataList[i][constants.FRIENDLINESS_RATE], dataList[i][constants.COMFORT_RATE])
                    #print("Var=", variance_dict)
                    #Error here
                    rated_chat += dataList[i][constants.CHAT_RATE] * variance_dict[constants.CHATTY_SCORE]
                    rated_safe += dataList[i][constants.SAFE_RATE] * variance_dict[constants.SAFETY_SCORE]
                    rated_punctual += dataList[i][constants.PUNCTUAL_RATE] * variance_dict[constants.PUNCTUALITY_SCORE]
                    rated_friend += dataList[i][constants.FRIENDLINESS_RATE] * variance_dict[constants.FRIENDLINESS_SCORE]
                    rated_comfort += dataList[i][constants.COMFORT_RATE] * variance_dict[constants.COMFORTIBILITY_SCORE]
                #print(rated_chat, rated_safe, rated_punctual, rated_friend, rated_comfort)
                #print("----------------------")

        class_dict = {constants.CHATTY_SCORE: rated_chat, constants.SAFETY_SCORE: rated_safe, constants.PUNCTUALITY_SCORE: rated_punctual,
                      constants.FRIENDLINESS_SCORE: rated_friend, constants.COMFORTIBILITY_SCORE: rated_comfort}
        max_score = max(class_dict.values())
        max_key = max(class_dict, key=class_dict.get)
        #print(class_dict)
        #print("for user", userid[j], "max_score_is", max_score, "with classifier ", max_key)
        #print("-----------------------------------------------------------------------------------------------")

        ridersndrivers = db.ridersndrivers
        ridersndrivers.find_one_and_update({constants.USER_ID: userid[j]},
                                           {"$set": {constants.FEEDBACK_GOT_CHAT: rated_chat,
                                                     constants.FEEDBACK_GOT_SAFE: rated_safe,
                                                     constants.FEEDBACK_GOT_PUNCTUAL: rated_punctual,
                                                     constants.FEEDBACK_GOT_FRIEND: rated_friend,
                                                     constants.FEEDBACK_GOT_COMFORT: rated_comfort,
                                                     constants.RATINGS_GOT_DICT: class_dict,
                                                     constants.GOT_FEEDBACK_CLASSIFIER: max_key
                                                     }})
        cursor = ridersndrivers.find({constants.USER_ID: userid[j]})
        list_data = list(cursor)
        got_fdbk_classifier_int = 0
        if max_key == constants.CHATTY_SCORE:
            got_fdbk_classifier_int = 1
        elif max_key == constants.SAFETY_SCORE:
            got_fdbk_classifier_int = 2
        elif max_key == constants.PUNCTUALITY_SCORE:
            got_fdbk_classifier_int = 3
        elif max_key == constants.FRIENDLINESS_SCORE:
            got_fdbk_classifier_int = 4
        elif max_key == constants.COMFORTIBILITY_SCORE:
            got_fdbk_classifier_int = 5

        got_fdbck_data = db.Got_Fdbck_Train
        cursor_check = got_fdbck_data.find({constants.USER_ID: userid[j]})
        check_list = list(cursor_check)
        #print(check_list)
        if check_list == [] or check_list == constants.EMPTY_STRING or check_list == None:
            train_fdbck_gotdocument = {
                constants.USER_ID: list_data[0][constants.USER_ID],
                constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                constants.RATINGS_GOT_DICT: class_dict,
                constants.UTT: list_data[0][constants.UTT],
                "max_rating_with_variance": max_score,
                constants.GOT_FEEDBACK_CLASSIFIER: max_key,
                constants.GOT_FEEDBACK_CLASSIFIER_INT: got_fdbk_classifier_int,
                constants.TIME_STAMP: datetime.now()
            }

            got_fdbck_id = got_fdbck_data.insert_one(train_fdbck_gotdocument)
        else:
            got_fdbck_data.find_one_and_update({constants.USER_ID: userid[j]},
                                                {"$set": {
                                                    constants.USER_ID: list_data[0][constants.USER_ID],
                                                    constants.MONGO_ID: list_data[0][constants.MONGO_ID],
                                                    constants.CHATTY_SCORE: list_data[0][constants.CHATTY_SCORE],
                                                    constants.SAFETY_SCORE: list_data[0][constants.SAFETY_SCORE],
                                                    constants.PUNCTUALITY_SCORE: list_data[0][constants.PUNCTUALITY_SCORE],
                                                    constants.FRIENDLINESS_SCORE: list_data[0][constants.FRIENDLINESS_SCORE],
                                                    constants.COMFORTIBILITY_SCORE: list_data[0][constants.COMFORTIBILITY_SCORE],
                                                    constants.RATINGS_GOT_DICT: class_dict,
                                                    constants.UTT: list_data[0][constants.UTT],
                                                    "max_rating_with_variance": max_score,
                                                    constants.GOT_FEEDBACK_CLASSIFIER: max_key,
                                                    constants.GOT_FEEDBACK_CLASSIFIER_INT: got_fdbk_classifier_int,
                                                    constants.TIME_STAMP: datetime.now()
                                                }})

    return constants.EMPTY_STRING

