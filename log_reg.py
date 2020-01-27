import pandas as pd
import numpy as np
from dbconnection import db
from sklearn import linear_model
from datetime import datetime
import constants
import random

def log_reg_given():
    print("-------------------------------------------------")
    resultCollectionFile = db.Give_Fdbck_Train
    cursor = resultCollectionFile.find()
    dateStr = datetime.now()
    resultStr = str(dateStr)
    resultStr = resultStr.replace(" ", "")
    df = pd.DataFrame(list(cursor))
    df.to_csv('give_feedback_train_data_1.csv', index=False)

    df = pd.read_csv('give_feedback_train_data_1.csv')
    #reg = linear_model.LinearRegression()
    reg = linear_model.LogisticRegression(penalty='l1',dual=False,max_iter=85, solver='liblinear', multi_class='auto')
    #reg = linear_model.LogisticRegression()
    reg.fit(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.giving_feedback_classifier_int)
    print("Log Regression Give Feedback Classifier Score is ", reg.score(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
               constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.giving_feedback_classifier_int))
    #print(reg.coef_)

    for i in range(0, 5):
        chat = random.randrange(1, 6)
        safe = random.randrange(1, 6)
        punctual = random.randrange(1, 6)
        friend = random.randrange(1, 6)
        comfort = random.randrange(1, 6)
        UTT_r = random.randrange(2, 6)
        UTT = UTT_r * 5
        print("New User UTT and Characteristics")
        print("[UTT, chat, safe, punctual, friend, comfort]")
        print([UTT, chat, safe, punctual, friend, comfort])
        classifier = reg.predict([[UTT, chat, safe, punctual, friend, comfort]])
        #print(classifier)
        value_classifier = classifier[0]
        round_classifier = round(value_classifier, 0)

        string_classifier = constants.EMPTY_STRING
        if round_classifier == 1:
            string_classifier = constants.CHATTY_SCORE
        elif round_classifier == 2:
            string_classifier = constants.SAFETY_SCORE
        elif round_classifier == 3:
            string_classifier = constants.PUNCTUALITY_SCORE
        elif round_classifier == 4:
            string_classifier = constants.FRIENDLINESS_SCORE
        elif round_classifier == 5:
            string_classifier = constants.COMFORTIBILITY_SCORE
        print("Give Feedback Classifer is ",round_classifier,  " or ", string_classifier)
        print("---------------------------------------------------")


def log_reg_got():
    print("-------------------------------------------------------------------")
    resultCollectionFile = db.Got_Fdbck_Train
    cursor = resultCollectionFile.find()
    dateStr = datetime.now()
    resultStr = str(dateStr)
    resultStr = resultStr.replace(" ", "")
    df = pd.DataFrame(list(cursor))
    df.to_csv('got_feedback_train_data_1.csv', index=False)

    df = pd.read_csv('got_feedback_train_data_1.csv')
    #reg = linear_model.LinearRegression()
    reg = linear_model.LogisticRegression(penalty='l1',dual=False,max_iter=85, solver='liblinear', multi_class='auto')
    #reg = linear_model.LogisticRegression()
    reg.fit(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int)
    print("Log Regression Got Feedback Classifier Score is ", reg.score(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
               constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int))
    #print(reg.coef_)

    for i in range(0, 5):
        chat = random.randrange(1, 6)
        safe = random.randrange(1, 6)
        punctual = random.randrange(1, 6)
        friend = random.randrange(1, 6)
        comfort = random.randrange(1, 6)
        UTT_r = random.randrange(2, 6)
        UTT = UTT_r * 5
        print("New User UTT and Characteristics")
        print("[UTT, chat, safe, punctual, friend, comfort]")
        print([UTT, chat, safe, punctual, friend, comfort])
        classifier = reg.predict([[UTT, chat, safe, punctual, friend, comfort]])
        #print(classifier)
        value_classifier = classifier[0]
        round_classifier = round(value_classifier, 0)

        string_classifier = constants.EMPTY_STRING
        if round_classifier == 1:
            string_classifier = constants.CHATTY_SCORE
        elif round_classifier == 2:
            string_classifier = constants.SAFETY_SCORE
        elif round_classifier == 3:
            string_classifier = constants.PUNCTUALITY_SCORE
        elif round_classifier == 4:
            string_classifier = constants.FRIENDLINESS_SCORE
        elif round_classifier == 5:
            string_classifier = constants.COMFORTIBILITY_SCORE
        print("Got Feedback Classifier is ", round_classifier, " or ", string_classifier)

log_reg_given()
log_reg_got()