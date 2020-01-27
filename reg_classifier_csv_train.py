import pandas as pd
import constants
from dbconnection import db
from bson.objectid import  ObjectId
from datetime import datetime

def reg_give():
    resultCollectionFile = db.Give_Fdbck_Train
    cursor = resultCollectionFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('give_feedback_train_data_1_v2.csv', index=False)
    df = pd.read_csv('give_feedback_train_data_1_v2.csv')
    train_dic = db.TheGiveTrainData
    train_dic.drop()

    #reg = BernoulliNB()
    #reg = RandomForestClassifier(n_estimators=10, max_depth=1)
    #reg = LinearRegression()
    #reg = LogisticRegression()
    #reg = MLPClassifier(solver='lbfgs', alpha=10, hidden_layer_sizes=(40,10), random_state=1)

    for index, row in df.iterrows():
        mongoId = row[constants.USER_ID]
        max_var = row["max_variance"]
        UTT = row[constants.UTT]
        chat = row[constants.CHATTY_SCORE]
        safe = row[constants.SAFETY_SCORE]
        punctual = row[constants.PUNCTUALITY_SCORE]
        friend = row[constants.FRIENDLINESS_SCORE]
        comfort = row[constants.COMFORTIBILITY_SCORE]
        giving_feedback_classifier = row[constants.GIVEN_FEEDBACK_CLASSIFIER]
        giving_feedback_classifier_int = row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT]

        collection = db.ridersndrivers
        cursor = collection.find({constants.MONGO_ID: ObjectId(mongoId)})
        dataList = list(cursor)

        reg_class = dataList[0][constants.REG_CLASSIFIER]

        reg_class_int = 0
        if reg_class == constants.CHATTY_SCORE:
            reg_class_int = 1
        if reg_class == constants.SAFETY_SCORE:
            reg_class_int = 2
        if reg_class == constants.PUNCTUALITY_SCORE:
            reg_class_int = 3
        if reg_class == constants.FRIENDLINESS_SCORE:
            reg_class_int = 4
        if reg_class == constants.COMFORTIBILITY_SCORE:
            reg_class_int = 5

        document = {
            constants.USER_ID: dataList[0][constants.USER_ID],
            "mongo_id": mongoId,
            "max_var": max_var,
            constants.UTT: UTT,
            constants.CHATTY_SCORE: chat,
            constants.SAFETY_SCORE: safe,
            constants.PUNCTUALITY_SCORE: punctual,
            constants.FRIENDLINESS_SCORE: friend,
            constants.COMFORTIBILITY_SCORE: comfort,
            constants.REG_CLASSIFIER: dataList[0][constants.REG_CLASSIFIER],
            "reg_classifier_int": reg_class_int,
            constants.GIVEN_FEEDBACK_CLASSIFIER: giving_feedback_classifier,
            constants.GIVEN_FEEDBACK_CLASSIFIER_INT: giving_feedback_classifier_int,
            constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING)
        }

        train_dic = db.TheGiveTrainData
        id = train_dic.insert_one(document)

    trainDataFile = db.TheGiveTrainData
    cursor = trainDataFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Give_Train_Data_2_More.csv', index=False)


def reg_got():
    df = pd.read_csv('got_feedback_train_data_1.csv')
    train_dic = db.TheGotTrainData
    train_dic.drop()

    #reg = BernoulliNB()
    #reg = RandomForestClassifier(n_estimators=10, max_depth=1)
    #reg = LinearRegression()
    #reg = LogisticRegression()
    #reg = MLPClassifier(solver='lbfgs', alpha=10, hidden_layer_sizes=(40,10), random_state=1)

    for index, row in df.iterrows():
        mongoId = row[constants.USER_ID]
        max_var = row["max_rating_with_variance"]
        UTT = row[constants.UTT]
        chat = row[constants.CHATTY_SCORE]
        safe = row[constants.SAFETY_SCORE]
        punctual = row[constants.PUNCTUALITY_SCORE]
        friend = row[constants.FRIENDLINESS_SCORE]
        comfort = row[constants.COMFORTIBILITY_SCORE]
        got_feedback_classifier = row[constants.GOT_FEEDBACK_CLASSIFIER]
        got_feedback_classifier_int = row[constants.GOT_FEEDBACK_CLASSIFIER_INT]
        collection = db.ridersndrivers
        cursor = collection.find({constants.MONGO_ID:ObjectId(mongoId)})
        dataList = list(cursor)

        reg_class = dataList[0][constants.REG_CLASSIFIER]
        reg_class_int = 0
        if reg_class == constants.CHATTY_SCORE:
            reg_class_int = 1
        if reg_class == constants.SAFETY_SCORE:
            reg_class_int = 2
        if reg_class == constants.PUNCTUALITY_SCORE:
            reg_class_int = 3
        if reg_class == constants.FRIENDLINESS_SCORE:
            reg_class_int = 4
        if reg_class == constants.COMFORTIBILITY_SCORE:
            reg_class_int = 5

        document = {
            constants.USER_ID: dataList[0][constants.USER_ID],
            "mongo_id": mongoId,
            "max_var": max_var,
            constants.UTT: UTT,
            constants.CHATTY_SCORE: chat,
            constants.SAFETY_SCORE: safe,
            constants.PUNCTUALITY_SCORE: punctual,
            constants.FRIENDLINESS_SCORE: friend,
            constants.COMFORTIBILITY_SCORE: comfort,
            constants.REG_CLASSIFIER: dataList[0][constants.REG_CLASSIFIER],
            "reg_classifier_int": reg_class_int,
            constants.GOT_FEEDBACK_CLASSIFIER: got_feedback_classifier,
            constants.GOT_FEEDBACK_CLASSIFIER_INT: got_feedback_classifier_int,
            constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING)
        }

        train_dic = db.TheGotTrainData
        id = train_dic.insert_one(document)

    trainDataFile = db.TheGotTrainData
    cursor = trainDataFile.find()
    df = pd.DataFrame(list(cursor))
    df.to_csv('The_Got_Train_Data_2_More.csv', index=False)

reg_give()
reg_got()

df = ravi
ravi_list = list(df)

print(ravi_list[[2,3])