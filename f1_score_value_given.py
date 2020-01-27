
import pandas as pd
import constants
from sklearn.metrics import confusion_matrix
import seaborn as sn
import scikitplot as skplt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from scipy import interp
from itertools import cycle
from matplotlib.backends.backend_pdf import PdfPages

def matrix_give():
    svm_model = "rfc_give__27000_no_UTT"
    testing_file = "give_feedback_train_data_11100.csv"
    predicted_file = "predicted_given_trained_data.csv"

    df_super_train = pd.read_csv(testing_file)
    #df_super_train = pd.read_csv('give_feedback_train_data_11100.csv')
    #df_super_train = pd.read_csv('The_Give_Train_Data_11000.csv')
    df_super_test = pd.read_csv(predicted_file)
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        strInt = row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT]
        computed.append(strInt)

    for index, row in df_super_test.iterrows():
        strInt = row[constants.GIVEN_FEEDBACK_CLASSIFIER_INT]
        predicted.append(strInt)
    print(confusion_matrix(computed, predicted))
    array = confusion_matrix(computed, predicted)
    x_axis_labels = ["Chatty", "Safety", "Punctuality", "Friendliness", "Comfortability"]  # labels for x-axis
    y_axis_labels = ["Chatty", "Safety", "Punctuality", "Friendliness", "Comfortability"] # labels for x-ax

    #Code for Confusion Mtrix
    df_cm = pd.DataFrame(array, range(5), range(5))
    sn.set(font_scale=2.5)  # for label size
    ax = sn.heatmap(df_cm, annot=True, fmt="d", annot_kws={"size": 30}, linewidths=0.5, xticklabels=x_axis_labels,
                    yticklabels=y_axis_labels)  # font size
    ax.set_ylim(5.0, 0)
    plt.xlabel("Actual or Computed Values", fontsize=30)
    plt.ylabel("Predicted Values", fontsize=30)
    plt.figure(figsize=(7, 3))
    plt.show()
    #plt.savefig('give_conf_matrix.pdf')


def matrix_got():
    svm_model = "rfc_got__27000_no_UTT"
    testing_file = "got_feedback_train_data_11100.csv"
    predicted_file = "predicted_got_trained_data.csv"
    df_super_train = pd.read_csv(testing_file)
    #df_super_train = pd.read_csv('got_feedback_train_data_11100.csv')
    #df_super_train = pd.read_csv('The_Got_Train_Data_11000.csv')
    df_super_test = pd.read_csv(predicted_file)
    computed = []
    predicted = []
    for index, row in df_super_train.iterrows():
        strInt = row[constants.GOT_FEEDBACK_CLASSIFIER_INT]
        computed.append(strInt)

    for index, row in df_super_test.iterrows():
        strInt = row[constants.GOT_FEEDBACK_CLASSIFIER_INT]
        predicted.append(strInt)


    print(confusion_matrix(computed, predicted))
    array = confusion_matrix(computed, predicted)
    x_axis_labels = ["Chatty", "Safety", "Punctuality", "Friendliness", "Comfortability"]  # labels for x-axis
    y_axis_labels = ["Chatty", "Safety", "Punctuality", "Friendliness", "Comfortability"]  # labels for x-ax
    #Code for Confusion Mtrix
    df_cm = pd.DataFrame(array, range(5), range(5))
    sn.set(font_scale=2.5)  # for label size
    ax = sn.heatmap(df_cm, annot=True, fmt="d", annot_kws={"size": 30}, linewidths=0.5, xticklabels=x_axis_labels,
                    yticklabels=y_axis_labels)  # font size
    ax.set_ylim(5.0, 0)
    plt.xlabel("Actual or Computed Values", fontsize=30)
    plt.ylabel("Predicted Values", fontsize=30)
    plt.figure(figsize=(7, 3))
    plt.show()
    #plt.savefig('give_conf_matrix.pdf')


#matrix_give()
matrix_got()