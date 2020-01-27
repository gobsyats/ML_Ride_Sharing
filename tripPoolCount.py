from dbconnection import db
import constants
from datetime import datetime
import pandas as pd
tripCollection = db.tripCollection
pool_completed = 0
pool_not_completed = 0
exact = 0
diff = 0
total_trip = 0
cursor = tripCollection.find()
listTrip = list(cursor)

for i in range(0, len(listTrip)):
    total_trip += 1
    pool_status = listTrip[i]["tripData"]["pool_completed"]
    exact_match = listTrip[i]["tripData"]["exact_match"]
    different_match = listTrip[i]["tripData"]["different_match"]
    pool_status = listTrip[i]["tripData"]["pool_completed"]
    #print(pool_status)
    if pool_status == constants.YES:
        pool_completed += 1
    elif pool_status == constants.NO:
        pool_not_completed += 1
    exact += exact_match
    diff += different_match

print("Total_Trips:", total_trip)
print("Pool Completed: ", pool_completed)
print("Pool Not Completed: ", pool_not_completed)

tripPoolDoc = {
    "total_trip": total_trip,
    "pool_completed": pool_completed,
    "pool_not_completed": pool_not_completed,
    "time_stamp": datetime.now().strftime(constants.TIME_STRING)

}

matchDoc = {
    "total_trip": total_trip,
    "exact_match": exact,
    "diff_matcj": diff,
    "time_stamp": datetime.now().strftime(constants.TIME_STRING)

}

tripPoolCount = db.tripPoolCount
id = tripPoolCount.insert_one(tripPoolDoc)


tripCharType = db.tripCharType
id = tripCharType.insert_one(matchDoc)

cursor = tripPoolCount.find()
df = pd.DataFrame(list(cursor))
df.to_csv('trip_Pool_count_v3.csv', index=False)

cursor2 = tripCharType.find()
df = pd.DataFrame(list(cursor2))
df.to_csv('trip_Match_Count_v3.csv', index=False)