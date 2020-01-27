#Simulation Code for registration
from datetime import datetime
import random
from dbconnection import db
import constants
import commons
import operator
import pandas as pd
import numpy as np
from dbconnection import db
import f1_score
from sklearn.svm import SVC
from datetime import datetime
import constants
import random
import pickle
import Defense_New_Make_Trip

#for userId in range(1, 100001):
#for userId in range(200001, 300001):
def gen_new_rider():
        userId = random.randrange(400001, 500001)
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
        print("Rider Userid: ", userId)
        print("User's Provided Characteristics: ", charDict)
        print("User's Provided UTT (mins): ", utt)
        print("Rider Registered successfully, predicting classifiers for riders...")
        rider_ids = ridersCollection.insert_one(riders)


        filename = "sup_1000_give"
        saved_given_reg = pickle.load(open(filename, 'rb'))
        classifier_super_test = saved_given_reg.predict([[utt, chattyScore, safetyScore,
                                                          punctualityScore, friendlinessScore, comfartabilityScore]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        string_give_novariance = convertor1(int_round_classifier_super_test)
        print("Without Variance Feedback-Give-Classifier is ", string_give_novariance)

        filename = "sup_1000_got"
        saved_given_reg = pickle.load(open(filename, 'rb'))
        classifier_super_test = saved_given_reg.predict([[utt, chattyScore, safetyScore,
                                                          punctualityScore, friendlinessScore, comfartabilityScore]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        string_got_novariance = convertor1(int_round_classifier_super_test)
        print("Without Variance Feedback-Received-Classifier is ", string_got_novariance)

        ridersCollection.find_one_and_update({constants.USER_ID: userId},
                                             {"$set": {
                                                 constants.GIVEN_FEEDBACK_CLASSIFIER: string_got_novariance,
                                                 constants.GOT_FEEDBACK_CLASSIFIER: string_got_novariance,
                                                 constants.FEEDBACK_GIVEN: constants.YES
                                             }})

        #Make 1st Trip
        Defense_New_Make_Trip.mainResults(userId, utt)


#count = ridersCollection.count_documents({})

#print('Found ', count, 'records')

def convertor1(int_round_classifier_super_test):
    string_give = ""
    if int_round_classifier_super_test == 1:

        string_give = constants.CHATTY_SCORE
    elif int_round_classifier_super_test == 2:
        string_give = constants.SAFETY_SCORE

    elif int_round_classifier_super_test == 3:
        string_give = constants.PUNCTUALITY_SCORE

    elif int_round_classifier_super_test == 4:
        string_give = constants.FRIENDLINESS_SCORE

    elif int_round_classifier_super_test == 5:
        string_give = constants.COMFORTIBILITY_SCORE

    return string_give



gen_new_rider()