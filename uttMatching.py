import constants
import commons
from datetime import datetime
from dbconnection import db

def UTTMatching(data):
        start_clock = datetime.now()
        #print("UTTDATA: ", data)
        #print("UTTDATA ends here")
        riders = data[0]
        #print("UTT_DATA Riders", riders)
        tripUTT = int(data[1])
        ridersMatching = int(data[2])
        ridersMatched = int(data[3])
        foundRiders = data[4]
        #print(foundRiders)
        tripSeatCapacity = int(data[5])
        seatCount = int(data[6])
        userSourceZone = data[7]
        source = data[8]
        destination = data[9]
        userIDQueue = data[10]
        locationlist = data[11]
        user_wait_start_time = data[12]
        userNoQueue = data[13]
        #print("--------------------------------------------")
        if foundRiders != [] or foundRiders != None:
            if foundRiders == None:
                print("None found")
                return None
            else:#print("-------------------------------------------------------------")
            #print("Working on Found Riders....")
                for i in range(0, len(foundRiders)):
                    end_clock = start_clock = datetime.now()
                    clock_diff_secs, clock_diff_mins = commons.time_diff(start_clock, end_clock)
                    #print("Clock Diff secs - ", clock_diff_secs, "mins - ", clock_diff_mins)
                    if i > 50:
                        print("i passed the rider count 50")
                        break
                        return None
                    else:
                        ridersMatching += 1
                        #print("no of riders checked are", ridersMatching)
                        # print("-------------------------------------------------------------------------")
                        if seatCount <= tripSeatCapacity - 2:
                            newRiderMongoId = foundRiders[i][constants.MONGO_ID]
                            newRiderUserId = foundRiders[i][constants.USER_ID]
                            newRiderUTT = foundRiders[i][constants.UTT]
                            newRiderZone = foundRiders[i][constants.CURRENT_ZONE]

                            if newRiderUTT <= tripUTT:
                                tripUTT = newRiderUTT
                                # print("UTT Updated to ", tripUTT)

                            random_new_user_source = ""
                            random_new_user_destination = ""
                            if newRiderZone == userSourceZone:
                                random_new_user_source = commons.generate_location(newRiderZone)
                            else:
                                random_new_user_source = commons.generate_random_location()

                            random_new_user_destination, lastZone \
                                = commons.generate_random_location_with_Zone()

                            while random_new_user_source == "":
                                if newRiderZone == userSourceZone:
                                    random_new_user_source = commons.generate_location(newRiderZone)
                                else:
                                    random_new_user_source = commons.generate_random_location()

                            while random_new_user_destination == "":
                                random_new_user_destination, lastZone = commons.generate_random_location_with_Zone()

                            # print(random_new_user_source, random_new_user_destination)
                            source_geocode_source, destination_geocode_source, new_user_distance_source, new_user_time_source = commons.google_Maps_time_distance(
                                source, random_new_user_source)
                            source_geocode_dest, destination_geocode_dest, new_user_distance_dest, new_user_time_dest = commons.google_Maps_time_distance(
                                destination, random_new_user_destination)

                            if new_user_time_source <= tripUTT:
                                if new_user_time_dest <= tripUTT:
                                    user_wait_end_time = datetime.now()
                                    user_wait_time_secs, user_wait_time_mins = commons.time_diff(user_wait_start_time, user_wait_end_time)
                                    user_wait_start_time = datetime.now()
                                    userIDQueue.append(newRiderMongoId)
                                    userNoQueue.append(newRiderUserId)
                                    seatCount += 1
                                    #print("SeatCount now", seatCount)
                                    print("------------------------------------------------------------------------------")
                                    print("**********User Satisfies Char and UTT Layer Conditions**************")
                                    ridersMatched += 1

                                    print("Total Driver's Vehicle Seating Capacity: ", tripSeatCapacity)
                                    print("Current Vehicle Capacity: ", seatCount)
                                    if(tripSeatCapacity-seatCount <= 1):
                                        print("Vehicle Reached the Seating Capacity, Pool Completed")
                                    rider = {constants.ROLE: constants.RIDER,
                                              constants.USER_ID: foundRiders[i][constants.USER_ID],
                                              # constants.SEAT_CAPACITY: cursorRandomUser[0][constants.SEAT_CAPACITY],
                                              constants.ALSO_DRIVER: foundRiders[i][constants.ALSO_DRIVER],
                                              constants.MONGO_ID: foundRiders[i][constants.MONGO_ID],
                                              constants.CHATTY_SCORE: foundRiders[i][constants.CHATTY_SCORE],
                                              constants.SAFETY_SCORE: foundRiders[i][constants.SAFETY_SCORE],
                                              constants.PUNCTUALITY_SCORE: foundRiders[i][constants.PUNCTUALITY_SCORE],
                                              constants.FRIENDLINESS_SCORE: foundRiders[i][constants.FRIENDLINESS_SCORE],
                                              constants.COMFORTIBILITY_SCORE: foundRiders[i][constants.COMFORTIBILITY_SCORE],
                                              constants.UTT: foundRiders[i][constants.UTT],
                                              constants.SOURCE: random_new_user_source,
                                              constants.DESTINATION: random_new_user_destination,
                                              constants.SOURCE_ADDRESS: destination_geocode_source,
                                              constants.DEST_ADDRESS: destination_geocode_dest,
                                              constants.USER_WAIT_TIME_MINS: user_wait_time_mins,
                                              constants.USER_WAIT_TIME_SECS: user_wait_time_secs,
                                              constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}
                                    print("Accepted Rider MongoID: ", foundRiders[i][constants.MONGO_ID])
                                    print("Accepted Rider UserID: ", foundRiders[i][constants.USER_ID])
                                    print("Accepted Rider Characteristics: ", foundRiders[i][constants.CHAR_DICT])

                                    riders = riders, rider
                                   #print("Printing Riders......", riders)
                                    # tripUTT = tripUTT - new_user_time_source
                                    #print("Trip UTT Reduced or Updated to minimal: ", tripUTT)
                                    userCollection = db.ridersndrivers
                                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
                                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                                       {"$set": {constants.BROADCASTING: constants.NO}})
                                    locationlist.append(random_new_user_source)
                                    locationlist.append(random_new_user_destination)
                                    user_wait_start_time = datetime.now()
                                    datareturn = [riders, tripUTT, userIDQueue, locationlist, ridersMatching, ridersMatched, lastZone, seatCount, user_wait_start_time, userNoQueue]
                                    return datareturn
                        else:
                            return None
                else:
                    return None
        else:
            return None


