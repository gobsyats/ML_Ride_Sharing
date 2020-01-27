import pandas as pd
from dbconnection import db
from sklearn.svm import SVC
from datetime import datetime
import constants
import pickle
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB


def log_reg_given():
    print("-------------------------------------------------")
    resultCollectionFile = db.Give_Fdbck_Train
    cursor = resultCollectionFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Give_Train_Data_27000.csv', index=False)
    df = pd.read_csv('The_Give_Train_Data_1.csv')
    #reg = linear_model.LogisticRegression(penalty='l1', dual=False, max_iter=110, solver='liblinear', multi_class='auto')
    reg = SVC(gamma=100, C=1000)
    #reg = KNeighborsClassifier()
    #reg=MultinomialNB()
    reg.fit(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                 constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.giving_feedback_classifier_int)
    print("Support Vector Machine Training Score for Give Feedback Classifier Score is ", reg.score(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
              constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.giving_feedback_classifier_int))
    print("Model Training Complete")
    #filename = "svm_given__20_Oct_All"
    filename = "svm_given_1000"
    save_given_reg = pickle.dump(reg, open(filename, 'wb'))

def log_reg_got():

    print("-------------------------------------------------------------------")
    resultCollectionFile = db.Got_Fdbck_Train
    cursor = resultCollectionFile.find()
    dateStr = datetime.now()
    resultStr = str(dateStr)
    resultStr = resultStr.replace(" ", "")
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Got_Train_Data_27000.csv', index=False)
    df = pd.read_csv('The_Got_Train_Data_1.csv')
    #reg = linear_model.LogisticRegression(penalty='l1', dual=False, max_iter=110, solver='liblinear', multi_class='auto')
    #reg = KNeighborsClassifier()
    reg = SVC(gamma=100, C=1000)
    #reg = MultinomialNB()
    reg.fit(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int)
    print("Support Vector Machine Training Score for Got Feedback Classifier Score is ", reg.score(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
              constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.got_feedback_classifier_int))

    print("Model Training Complete")
    #filename = "svm_got__20_Oct_All"
    filename = "svm_got_1000"
    save_got_reg = pickle.dump(reg, open(filename, 'wb'))

log_reg_given()
log_reg_got()


import supVM_test
supVM_test.supVM_given_test()
supVM_test.supVM_got_test()