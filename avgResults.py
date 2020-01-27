from dbconnection import db
import constants
from datetime import datetime

def avgWaitingTime():
    tripCollection = db.tripCollection
    trip_formation_time = 0
    total_trip = 0
    cursor = tripCollection.find()
    listTrip = list(cursor)

    for i in range(0, len(listTrip)):
        total_trip += 1
        trip_formation_time += listTrip[i]["tripData"][constants.TRIP_DIFF_MINS]

    return trip_formation_time, total_trip


trip_formation_time, total_trip = avgWaitingTime()
avg_time = trip_formation_time/total_trip

print("Total Trip Count:", total_trip)
print("Total Trip Formation Time: ", trip_formation_time)
print("Avg Trip Formation Time: ", avg_time)
print("Time_Stamp: ", datetime.now().strftime(constants.TIME_STRING))

tripPoolDoc = {
    "document": "result",
    "type": "avg_trip_formation_time",
    "total_trip_count": total_trip,
    "all_trips_formation_time": trip_formation_time,
    "avg_waiting_time": avg_time,
    "time_stamp": datetime.now().strftime(constants.TIME_STRING)
}

tripPoolCount = db.tripPoolCount
id = tripPoolCount.insert_one(tripPoolDoc)