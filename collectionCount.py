from dbconnection import db

from dbconnection import db

ridersndrivers = db.ridersndrivers
r_count = ridersndrivers.count()
print("ridersndriver count is ", r_count)


zone_latlon = db.zone_latlon
latloncount = zone_latlon.count()
print("lat_lon count is ", latloncount)

zone_lookup = db.zone_lookup
lookup_count = zone_lookup.count()
print("lookup_count is ", lookup_count)

zonenlocations = db.zonenlocations
zone_location = zonenlocations.count()
print("zonelocation count is  ", zone_location)

resultsCollection = db.resultsCollection
result_count = resultsCollection.count()
print("resultCollection count is ", result_count)

tripCollection = db.tripCollection
nooftrips = tripCollection.count()
print("trip count is ", nooftrips)

feedbackCollection = db.feedbackCollection
fdback_count = feedbackCollection.count()
print("feedback_collection count is ", fdback_count)

Give_Fdbck_Train = db.Give_Fdbck_Train
give_fdbck_count = Give_Fdbck_Train.count()
print("Give Feedback count is ", give_fdbck_count)

Got_Fdbck_Train = db.Got_Fdbck_Train
got_fdbck_count = Got_Fdbck_Train.count()
print("Got Feedback count is ", got_fdbck_count)
