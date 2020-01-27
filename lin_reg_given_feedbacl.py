import pandas as pd
from dbconnection import db
from sklearn import linear_model
from datetime import  datetime
import constants
import random

give_fdbck_data = db.Give_Fdbck_Train
cursor = give_fdbck_data.find()
dateStr = datetime.now()
resultStr = str(dateStr)
resultStr = resultStr.replace(" ", "")
df = pd.DataFrame(list(cursor))
df.to_csv('give_fdbck_data_v1.csv', index=False)

df = pd.read_csv('give_fdbck_data_v1.csv')

#reg = linear_model.LogisticRegression()
reg = linear_model.LogisticRegression(penalty='l1',dual=False,max_iter=110, solver='liblinear', multi_class='auto')
reg.fit(df[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
            constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]], df.given_feedback_classifier_int)
#print(reg.coef_)

for i in range(0, 3):
    chat = random.randrange(1,6)
    safe = random.randrange(1, 6)
    punctual = random.randrange(1, 6)
    friend = random.randrange(1, 6)
    comfort = random.randrange(1, 6)
    UTT_r = random.randrange(2, 6)
    UTT = UTT_r * 5
    print([UTT, chat, safe, punctual, friend, comfort])
    classifier = reg.predict([[UTT, chat, safe, punctual, friend, comfort]])
    #print(classifier[0])
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
    print("Predicted User Sentiment is ", round_classifier, "string view is ", string_classifier)



