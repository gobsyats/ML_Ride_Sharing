import statistics
import constants
from datetime import datetime
from dbconnection import db
chat = [0, 0, 2]
safe = [1, 0, 4]
punctual = [0, 0, 0]
friend = [0, 0, 2]
comfort = [1, 0, 0]

userid = 21
mongoId = 12828189
chat_reg = 2
safe_reg = 1
punctual_reg = 4
friend_reg = 2
comfort_reg = 4

# Prints variance of the sample set

# Function will automatically calulate
# it's mean and set it as xbar
print("Variance of chat set is % s"
      % (statistics.variance(chat)))
print("Variance of safe set is % s"
      % (statistics.variance(safe)))
print("Variance of punctual set is % s"
      % (statistics.variance(punctual)))
print("Variance of friend set is % s"
      % (statistics.variance(friend)))
print("Variance of comfort set is % s"
      % (statistics.variance(comfort)))

datalist = {
    constants.CHATTY_SCORE: statistics.variance(chat),
    constants.SAFETY_SCORE: statistics.variance(safe),
    constants.PUNCTUALITY_SCORE: statistics.variance(punctual),
    constants.FRIENDLINESS_SCORE: statistics.variance(friend),
    constants.COMFORTIBILITY_SCORE: statistics.variance(comfort)
    }
maxof = max(datalist, key=datalist.get)
print("User Focusses on", maxof)

# document = {
#     constants.USER_ID: userid,
#     constants.MONGO_ID: "12828189",
#     constants.CHATTY_SCORE: chat_reg,
#     constants.SAFETY_SCORE: safe_reg,
#     constants.PUNCTUALITY_SCORE: punctual_reg,
#     constants.FRIENDLINESS_SCORE: friend_reg,
#     constants.COMFORTIBILITY_SCORE: comfort_reg,
#     constants.TIME_STAMP: datetime.now().strftime(constants.TIME_STRING)
#
# }
#
# model_train_data = db.model_train_data
# model_id = model_train_data.insert_one(document)


