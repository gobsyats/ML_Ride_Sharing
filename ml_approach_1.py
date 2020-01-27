import pandas as pd
import numpy as np
from dbconnection import db
from sklearn import linear_model
from datetime import  datetime
import constants

resultCollectionFile = db.feedbackCollection
cursor = resultCollectionFile.find()
dateStr = datetime.now()
resultStr = str(dateStr)
resultStr = resultStr.replace(" ", "")
df = pd.DataFrame(list(cursor))
df.to_csv('sample_feedback_v6.csv', index=False)

df = pd.read_csv('sample_feedback_v6.csv')

reg = linear_model.LinearRegression()
reg.fit(df[[constants.CHAT_RATE, constants.SAFE_RATE, constants.PUNCTUAL_RATE,
            constants.FRIENDLINESS_RATE, constants.COMFORT_RATE]], df.feedback_given_classifier_to_int)
#print(reg.coef_)

classifier = reg.predict([[2, 4, 3, 5, 1]])
print(classifier)

