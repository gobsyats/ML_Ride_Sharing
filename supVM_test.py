import pandas as pd
import numpy as np
from dbconnection import db
import f1_score
from sklearn.svm import SVC
from datetime import datetime
import constants
import random
import pickle

def supVM_given_test():
    print("----------------------------Testing Give SUPVM---------------------------------------")
    filename = "rfc_give__27000_no_UTT"
    testing_file = "give_feedback_train_data_11100.csv"
    #saved_given_reg = pickle.load(open("rfc_give__27000_no_UTT", 'rb'))
    saved_given_reg = pickle.load(open(filename, 'rb'))
    #saved_given_reg = pickle.load(open("rfc_give__27000_no_UTT_Sayali", 'rb'))
    print("Model Retrieved")
    print("Performing F1 Score Test...")
    Give_Fdbck_Test_F1 = db.Give_Fdbck_Test_F1
    Give_Fdbck_Test_F1.drop()
    df_super_test = pd.read_csv(testing_file)
    print("Predicting Values Now...")
    for index, row in df_super_test.iterrows():
        chat_super_test = row[constants.CHATTY_SCORE]
        safe_super_test = row[constants.SAFETY_SCORE]
        punctual_super_test = row[constants.PUNCTUALITY_SCORE]
        friend_super_test = row[constants.FRIENDLINESS_SCORE]
        comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
        UTT_super_test = row[constants.UTT]
        variance = row["max_variance"]
        #variance = row["max_var"]
        #reg_classifer = row["reg_classifier_int"]
        #classifier_super_test = saved_given_reg.predict([[reg_classifer, UTT_super_test, chat_super_test, safe_super_test, punctual_super_test, friend_super_test, comfort_super_test]])
        classifier_super_test = saved_given_reg.predict([[variance, UTT_super_test, chat_super_test, safe_super_test,
                                                          punctual_super_test, friend_super_test, comfort_super_test]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)

        super_test_document = {
            "max_variance": variance,
            #"reg_classifier": reg_classifer,
            constants.UTT: UTT_super_test,
            constants.CHATTY_SCORE: chat_super_test,
            constants.SAFETY_SCORE: safe_super_test,
            constants.PUNCTUALITY_SCORE: punctual_super_test,
            constants.FRIENDLINESS_SCORE: friend_super_test,
            constants.COMFORTIBILITY_SCORE: comfort_super_test,
            constants.GIVEN_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
        }
        super_test_given_test_data = db.Give_Fdbck_Test_F1
        id_f1 = super_test_given_test_data.insert_one(super_test_document)
    super_test_given_test_data = db.Give_Fdbck_Test_F1
    cursor_super = super_test_given_test_data.find()
    df_test_csv = pd.DataFrame(list(cursor_super))
    df_test_csv.to_csv('predicted_given_trained_data.csv', index=False)
    f1_score.f1_score_given(filename, testing_file, 'predicted_given_trained_data.csv', classifier_super_test)


def supVM_got_test():
    filename = "rfc_got__27000_no_UTT"
    testing_file = "got_feedback_train_data_11100.csv"
    #saved_got_reg = pickle.load(open("rfc_got__27000_no_UTT", 'rb'))
    saved_got_reg = pickle.load(open(filename, 'rb'))
    print("----------------------------Testing Got SUPVM---------------------------------------")
    #saved_got_reg = pickle.load(open("rfc_got__27000_no_UTT_Sayali", 'rb'))
    print("Model Retrieved")
    print("Performing F1 Score Test...")
    Got_Fdbck_Test_F1 = db.Got_Fdbck_Test_F1
    Got_Fdbck_Test_F1.drop()
    df_super_test = pd.read_csv(testing_file)
    print("Predicting Values Now...")
    for index, row in df_super_test.iterrows():
        chat_super_test = row[constants.CHATTY_SCORE]
        safe_super_test = row[constants.SAFETY_SCORE]
        punctual_super_test = row[constants.PUNCTUALITY_SCORE]
        friend_super_test = row[constants.FRIENDLINESS_SCORE]
        comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
        UTT_super_test = row[constants.UTT]
        variance = row["max_rating_with_variance"]
        #variance = row["max_variance"]
        #reg_classifer = row["reg_classifier_int"]

        #print(UTT_super_test, chat_super_test, safe_super_test, punctual_super_test, friend_super_test, comfort_super_test)
        #classifier_super_test = saved_got_reg.predict([[reg_classifer, UTT_super_test, chat_super_test, safe_super_test, punctual_super_test, friend_super_test, comfort_super_test]])
        classifier_super_test = saved_got_reg.predict([[variance, UTT_super_test, chat_super_test, safe_super_test,
                                                        punctual_super_test, friend_super_test, comfort_super_test]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        super_test_document = {
            "variance": variance,
            constants.UTT: UTT_super_test,
            constants.CHATTY_SCORE: chat_super_test,
            constants.SAFETY_SCORE: safe_super_test,
            constants.PUNCTUALITY_SCORE: punctual_super_test,
            constants.FRIENDLINESS_SCORE: friend_super_test,
            constants.COMFORTIBILITY_SCORE: comfort_super_test,
            constants.GOT_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
        }
        super_test_got_test_data = db.Got_Fdbck_Test_F1
        id_f1 = super_test_got_test_data.insert_one(super_test_document)
    super_test_got_test_data = db.Got_Fdbck_Test_F1
    cursor_super = super_test_got_test_data.find()
    df_test_csv = pd.DataFrame(list(cursor_super))
    df_test_csv.to_csv('predicted_got_trained_data.csv', index=False)
    f1_score.f1_score_got(filename, testing_file, 'predicted_got_trained_data.csv', classifier_super_test)

supVM_given_test()
supVM_got_test()