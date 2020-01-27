import pandas as pd
import numpy as np
from dbconnection import db
from sklearn import linear_model
from sklearn.svm import SVC
from datetime import datetime
import constants
import random
import pickle

df_super_test = pd.read_csv('give_feedback_train_data_full.csv')
chat_super_test = df_super_test[constants.CHATTY_SCORE]
#print(chat_super_test)

for index, row in df_super_test.iterrows():
    print(row[constants.CHATTY_SCORE])
# safe_super_test =
# punctual_super_test =
# friend_super_test =
# comfort_super_test =