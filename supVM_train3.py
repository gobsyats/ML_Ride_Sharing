import pandas as pd
from dbconnection import db
from sklearn.svm import SVC
from datetime import datetime
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier
import constants
import pickle
from sklearn.ensemble import RandomForestClassifier
from dbconnection import db
from bson.objectid import  ObjectId
from datetime import  datetime

def log_reg_given():
    print("-------------------------------------------------")
    #df = pd.read_csv('give_feedback_train_data_1.csv')
    df = pd.read_csv('The_Give_Train_Data_27000.csv')


    #reg = BernoulliNB()
    #reg = RandomForestClassifier(n_estimators=10, max_depth=1)
    #reg = LinearRegression()
    #reg = LogisticRegression()
    #reg = MLPClassifier(solver='lbfgs', alpha=10, hidden_layer_sizes=(40,10), random_state=1)

    reg = SVC(gamma=100, C=1000)
    reg.fit(df[["reg_classifer_int", constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.giving_feedback_classifier_int)
    print("Support Vector Machine Training Score for Give Feedback Classifier Score is ",
         reg.score(df[["reg_classifer_int", constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                       constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]],
                    df.giving_feedback_classifier_int))
    print("Model Training Complete")
    filename = "svm_27000_reg_give"
    save_given_reg = pickle.dump(reg, open(filename, 'wb'))


def log_reg_got():
    print("-------------------------------------------------------------------")
    #df = pd.read_csv('got_feedback_train_data_1.csv')
    df = pd.read_csv('The_Got_Train_Data_27000.csv')
    reg = SVC(gamma=100, C=1000)
    #reg = BernoulliNB()
    #reg = RandomForestClassifier(n_estimators=10, max_depth=1)
    #reg = LogisticRegression()
    #reg = LinearRegression()
    #reg = MLPClassifier(solver='lbfgs', alpha=10, hidden_layer_sizes=(5, 2), random_state=1)
    reg.fit(df[["reg_classifer_int", constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int)
    print("Support Vector Machine Training Score for Got Feedback Classifier Score is ",
          reg.score(df[["reg_classifer_int", constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                        constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int))
    print("Model Training Complete")
    filename = "svm_27000_reg_got"
    save_got_reg = pickle.dump(reg, open(filename, 'wb'))

log_reg_given()
log_reg_got()


import supVM_test
supVM_test.supVM_given_test()
supVM_test.supVM_got_test()