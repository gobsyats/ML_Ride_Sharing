from dbconnection import db

ridersndrivers = db.ridersndrivers
ridersndrivers.drop()

zone_latlon = db.zone_latlon
zone_latlon.drop()

zone_lookup = db.zone_lookup
zone_lookup.drop()

zonenlocations = db.zonenlocations
zonenlocations.drop()

zonenlocations = db.zonenlocations
zonenlocations.drop()

resultsCollection = db.resultsCollection
resultsCollection.drop()

tripCollection = db.tripCollection
tripCollection.drop()

feedbackCollection = db.feedbackCollection
feedbackCollection.drop()

Give_Fdbck_Train = db.Give_Fdbck_Train
Give_Fdbck_Train.drop()

Got_Fdbck_Train = db.Got_Fdbck_Train
Got_Fdbck_Train.drop()
