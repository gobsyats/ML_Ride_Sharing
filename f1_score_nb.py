from sklearn.metrics import f1_score
import pandas as pd
import constants
from sklearn.metrics import mean_squared_error
from math import sqrt


def f1_score_given():
    df_super_train = pd.read_csv('give_feedback_train_data_New_Full.csv')
    df_super_test = pd.read_csv('predicted_given_trained_data_nb.csv')
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        computed.append(row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT])

    for index, row in df_super_test.iterrows():
        predicted.append(row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT])

    rmse = sqrt(mean_squared_error(computed, predicted))
    print("F1 Score Feedback Given Classifier:", f1_score(computed, predicted, average='weighted'))
    print("Root Mean Sqaure Error Feedback Given Classifier", rmse)

def f1_score_got():
    df_super_train = pd.read_csv('got_feedback_train_data_New_Full.csv')
    df_super_test = pd.read_csv('predicted_got_trained_data_nb.csv')
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        computed.append(row[constants.GOT_FEEDBACK_CLASSIFIER_INT])

    for index, row in df_super_test.iterrows():
        predicted.append(row[constants.GOT_FEEDBACK_CLASSIFIER_INT])

    rmse = sqrt(mean_squared_error(computed, predicted))
    print("F1 Score Feedback Got Classifier:", f1_score(computed, predicted, average='weighted'))
    print("Root Mean Sqaure Error Feedback Got Classifier", rmse)


