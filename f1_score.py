from sklearn.metrics import f1_score
import pandas as pd
import constants
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.metrics import accuracy_score
from datetime import datetime
from dbconnection import db
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
import scikitplot as skplt
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

import numpy as np
def f1_score_given(svm_model, testing_file, predicted_file):
    df_super_train = pd.read_csv(testing_file)
    #df_super_train = pd.read_csv('give_feedback_train_data_11100.csv')
    #df_super_train = pd.read_csv('The_Give_Train_Data_11000.csv')
    df_super_test = pd.read_csv(predicted_file)
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        computed.append(row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT])

    for index, row in df_super_test.iterrows():
        predicted.append(row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT])

    target_names = ["chatty", "safety", "punctuality", "friendliness", "comfortibility"]

    rmse = sqrt(mean_squared_error(computed, predicted))
    f1_score_imp =  f1_score(computed, predicted, average='weighted', labels=np.unique(predicted))
    accuracy_score_imp = accuracy_score(computed, predicted)
    f1_score_each_class = list(f1_score(computed, predicted, average=None, labels=np.unique(predicted)))
    recall = list(recall_score(computed, predicted, average=None))
    precision = list(precision_score(computed, predicted, average=None))
    print("F1 Score Feedback Given Classifier:", f1_score_imp)
    print("F1 Score None Given Classifier:", f1_score_each_class)
    print("Root Mean Sqaure Error Feedback Given Classifier", rmse)
    print("Accuracy Score is ", accuracy_score_imp)
    print("Recall Score is ", recall)
    print("Precision Score is ", precision)
    print(classification_report(computed, predicted, target_names=target_names))

    test_doc = {
        constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
        "svm_model_name": svm_model,
        "testing_file": testing_file,
        "feedback_type": "given",
        "type_test": "20000 Records",
        "f1_score": f1_score_imp,
        "f1_score_class": f1_score_each_class,
        "root_mean_sqaure": rmse,
        "accuracy_score": accuracy_score_imp,
        "recall": recall,
        "precision": precision
    }
    ml_score_collection = db.ML_Score_Collection
    id_ml = ml_score_collection.insert_one(test_doc)


def f1_score_got(svm_model, testing_file, predicted_file):
    target_names = ["chatty", "safety", "punctuality", "friendliness", "comfortibility"]
    df_super_train = pd.read_csv(testing_file)
    #df_super_train = pd.read_csv('got_feedback_train_data_11100.csv')
    #df_super_train = pd.read_csv('The_Got_Train_Data_11000.csv')
    df_super_test = pd.read_csv(predicted_file)
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        computed.append(row[constants.GOT_FEEDBACK_CLASSIFIER_INT])

    for index, row in df_super_test.iterrows():
        predicted.append(row[constants.GOT_FEEDBACK_CLASSIFIER_INT])

    rmse = sqrt(mean_squared_error(computed, predicted))
    f1_score_imp = f1_score(computed, predicted, average='weighted', labels=np.unique(predicted))
    accuracy_score_imp = accuracy_score(computed, predicted)
    f1_score_each_class = list(f1_score(computed, predicted, average=None, labels=np.unique(predicted)))
    recall = list(recall_score(computed, predicted, average=None))
    precision = list(precision_score(computed, predicted, average=None))

    print("F1 Score Feedback Given Classifier:", f1_score_imp)
    print("F1 Score None Given Classifier:", f1_score_each_class)
    print("Root Mean Sqaure Error Feedback Given Classifier", rmse)
    print("Accuracy Score is ", accuracy_score_imp)
    print("Recall Score is ", recall)
    print("Precision Score is ", precision)
    print(classification_report(computed, predicted, target_names=target_names))

    test_doc = {
        constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING),
        "svm_model_name": svm_model,
        "testing_file": testing_file,
        "feedback_type": "got",
        "type_test": "20000 Records",
        "f1_score": f1_score_imp,
        "f1_score_class": f1_score_each_class,
        "root_mean_sqaure": rmse,
        "accuracy_score": accuracy_score_imp,
        "recall": recall,
        "precision": precision
    }
    ml_score_collection = db.ML_Score_Collection
    id_ml = ml_score_collection.insert_one(test_doc)



