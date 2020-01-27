import pandas as pd
from dbconnection import db
import f1_score_nb
import constants
import pickle

def nb_given_test():
    print("----------------------------Testing Give NB---------------------------------------")
    saved_given_reg = pickle.load(open("save_given_nb_v1", 'rb'))
    print("Model Retrieved")
    print("Performing F1 Score Test...")
    Give_Fdbck_Test_NB_F1 = db.Give_Fdbck_Test_NB_F1
    Give_Fdbck_Test_NB_F1.drop()
    df_super_test = pd.read_csv('give_feedback_train_data_New_Full.csv')
    print("Predicting Values Now...")
    for index, row in df_super_test.iterrows():
        chat_super_test = row[constants.CHATTY_SCORE]
        safe_super_test = row[constants.SAFETY_SCORE]
        punctual_super_test = row[constants.PUNCTUALITY_SCORE]
        friend_super_test = row[constants.FRIENDLINESS_SCORE]
        comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
        UTT_super_test = row[constants.UTT]
        classifier_super_test = saved_given_reg.predict([[UTT_super_test, chat_super_test, safe_super_test, punctual_super_test, friend_super_test, comfort_super_test]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        super_test_document = {
            constants.UTT: UTT_super_test,
            constants.CHATTY_SCORE: chat_super_test,
            constants.SAFETY_SCORE: safe_super_test,
            constants.PUNCTUALITY_SCORE: punctual_super_test,
            constants.FRIENDLINESS_SCORE: friend_super_test,
            constants.COMFORTIBILITY_SCORE: comfort_super_test,
            constants.GIVEN_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
        }
        super_test_given_test_data = db.Give_Fdbck_Test_NB_F1
        id_f1 = super_test_given_test_data.insert_one(super_test_document)
    super_test_given_test_data = db.Give_Fdbck_Test_NB_F1
    cursor_super = super_test_given_test_data.find()
    df_test_csv = pd.DataFrame(list(cursor_super))
    df_test_csv.to_csv('predicted_given_trained_data_nb.csv', index=False)
    f1_score_nb.f1_score_given()


def nb_got_test():

    print("----------------------------Testing Got NB---------------------------------------")
    saved_got_reg = pickle.load(open("save_got_nb_v1", 'rb'))
    print("Model Retrieved")
    print("Performing F1 Score Test...")
    Got_Fdbck_Test_F1 = db.Got_Fdbck_Test_NB_F1
    Got_Fdbck_Test_F1.drop()
    df_super_test = pd.read_csv('got_feedback_train_data_New_Full.csv')
    print("Predicting Values Now...")
    for index, row in df_super_test.iterrows():
        chat_super_test = row[constants.CHATTY_SCORE]
        safe_super_test = row[constants.SAFETY_SCORE]
        punctual_super_test = row[constants.PUNCTUALITY_SCORE]
        friend_super_test = row[constants.FRIENDLINESS_SCORE]
        comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
        UTT_super_test = row[constants.UTT]
        classifier_super_test = saved_got_reg.predict([[UTT_super_test, chat_super_test, safe_super_test,
                                                          punctual_super_test, friend_super_test, comfort_super_test]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        super_test_document = {
            constants.UTT: UTT_super_test,
            constants.CHATTY_SCORE: chat_super_test,
            constants.SAFETY_SCORE: safe_super_test,
            constants.PUNCTUALITY_SCORE: punctual_super_test,
            constants.FRIENDLINESS_SCORE: friend_super_test,
            constants.COMFORTIBILITY_SCORE: comfort_super_test,
            constants.GOT_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
        }
        super_test_got_test_data = db.Got_Fdbck_Test_NB_F1
        id_f1 = super_test_got_test_data.insert_one(super_test_document)
    super_test_got_test_data = db.Got_Fdbck_Test_NB_F1
    cursor_super = super_test_got_test_data.find()
    df_test_csv = pd.DataFrame(list(cursor_super))
    df_test_csv.to_csv('predicted_got_trained_data_nb.csv', index=False)
    f1_score_nb.f1_score_got()


#nb_given_test()
#nb_got_test()