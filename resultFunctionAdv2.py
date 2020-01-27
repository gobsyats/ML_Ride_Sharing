from dbconnection import db
import random
import constants
from datetime import datetime
import commons

def mainResults(parameterUTT, forriders):
    exact_close_match = 0
    different_char_match = 0
    matching_type = ""
    start_time = datetime.now().strftime(constants.TIME_STRING)
    start_time_actual = datetime.now()
    userCollection = db.ridersndrivers
    randomUserID = random.randrange(1, constants.TOTAL_USERS)
    # print("randomUserId is ", randomUserID)
    # Find 1 Random User
    cursor = userCollection.find({constants.USER_ID: randomUserID, constants.ACTIVE_STATE: constants.NO,
                                  constants.ALSO_DRIVER: constants.NO, constants.BROADCASTING: constants.YES,
                                  constants.UTT: parameterUTT})
    cursorRandomUser = list(cursor)
    # print(cursorRandomUser)
    ridersMatching = 1
    ridersMatched = 0
    requiredDrivers = 0
    userIDQueue = []
    destinationList = []
    trip = {}
    driver = {}
    first_rider = {}
    riders = {}
    locationlist = []
    tripUTT = 0

    # Finds Only Inactive and Broacasting Rider - A True Broadcasting Rider
    while cursorRandomUser == []:
        randomUserID = random.randrange(1, constants.TOTAL_USERS)
        # print("randomUserId is ", randomUserID)
        cursor = userCollection.find({constants.USER_ID: randomUserID, constants.ACTIVE_STATE: constants.NO,
                                      constants.ALSO_DRIVER: constants.NO, constants.BROADCASTING: constants.YES,
                                      constants.UTT: parameterUTT})
        cursorRandomUser = list(cursor)

    tripUTT = cursorRandomUser[0][constants.UTT]

    first_rider = {constants.ROLE: constants.RIDER,
                   constants.USER_ID: cursorRandomUser[0][constants.USER_ID],
                   # constants.SEAT_CAPACITY: cursorRandomUser[0][constants.SEAT_CAPACITY],
                   constants.ALSO_DRIVER: cursorRandomUser[0][constants.ALSO_DRIVER],
                   constants.MONGO_ID: cursorRandomUser[0][constants.MONGO_ID],
                   constants.CHATTY_SCORE: cursorRandomUser[0][constants.CHATTY_SCORE],
                   constants.SECURITY_SCORE: cursorRandomUser[0][constants.SECURITY_SCORE],
                   constants.PUNCTUALITY_SCORE: cursorRandomUser[0][constants.PUNCTUALITY_SCORE],
                   constants.FRIENDLINESS_SCORE: cursorRandomUser[0][constants.FRIENDLINESS_SCORE],
                   constants.COMFORTIBILITY_SCORE: cursorRandomUser[0][constants.COMFORTIBILITY_SCORE],
                   constants.UTT: cursorRandomUser[0][constants.UTT],
                   constants.CURRENT_ZONE: cursorRandomUser[0][constants.CURRENT_ZONE],
                   constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}
    Broadcasting_userId = cursorRandomUser[0][constants.MONGO_ID]
    userIDQueue.append(Broadcasting_userId)
    userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
    userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       {"$set": {constants.BROADCASTING: constants.NO}})
    userSourceZone = cursorRandomUser[0][constants.CURRENT_ZONE]
    userSourceLocation = cursorRandomUser[0][constants.CURRENT_LOCATION]
    tripSeatCapacity = 0
    tripChatty = cursorRandomUser[0][constants.CHATTY_SCORE]
    tripSecurity = cursorRandomUser[0][constants.SECURITY_SCORE]
    tripPunctuality = cursorRandomUser[0][constants.PUNCTUALITY_SCORE]
    tripFriendliness = cursorRandomUser[0][constants.FRIENDLINESS_SCORE]
    tripComfortibility = cursorRandomUser[0][constants.COMFORTIBILITY_SCORE]

    print("Broadcasting rider details")
    print(first_rider)

    # Generate 2 Locations
    # Get Distance and Time between Source and Destinations

    # Generate Random Sourece Zone and Get A Random Source Location
    locations = db.zonenlocations
    source = commons.generate_location(userSourceZone)

    # Generate Random Destination Zone and Pick Random Location
    destination = commons.generate_random_location()

    locationlist.append(destination)

    print("------------------------------------------------------------------------------------------------")
    print("Printing User's Broadcasting Locations and Trip Details.....")
    # Using Google Map Apis
    print("User Source Zone = ", userSourceZone)
    source_geocode, destination_gecode, total_trip_distance, total_time_2_int = commons.google_Maps_time_distance(
        source, destination)
    print("Trip UTT = ", tripUTT)
    print("Total Trip Time with UTT = ", total_time_2_int + tripUTT)
    # print(source_geocode)
    # print(destination_gecode)
    # print(total_trip_distance)
    # print(total_time_2_int)
    # print(tripUTT)
    # print(total_time_2_int + tripUTT)

    first_rider = {constants.ROLE: constants.RIDER,
                   constants.USER_ID: cursorRandomUser[0][constants.USER_ID],
                   # constants.SEAT_CAPACITY: cursorRandomUser[0][constants.SEAT_CAPACITY],
                   constants.ALSO_DRIVER: cursorRandomUser[0][constants.ALSO_DRIVER],
                   constants.MONGO_ID: cursorRandomUser[0][constants.MONGO_ID],
                   constants.CHATTY_SCORE: cursorRandomUser[0][constants.CHATTY_SCORE],
                   constants.SECURITY_SCORE: cursorRandomUser[0][constants.SECURITY_SCORE],
                   constants.PUNCTUALITY_SCORE: cursorRandomUser[0][constants.PUNCTUALITY_SCORE],
                   constants.FRIENDLINESS_SCORE: cursorRandomUser[0][constants.FRIENDLINESS_SCORE],
                   constants.COMFORTIBILITY_SCORE: cursorRandomUser[0][constants.COMFORTIBILITY_SCORE],
                   constants.UTT: cursorRandomUser[0][constants.UTT],
                   constants.SOURCE: source,
                   constants.DESTINATION: destination,
                   constants.SOURCE_ADDRESS: source_geocode,
                   constants.DEST_ADDRESS: destination_gecode,
                   constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}

    # #Search Drivers in 2 minutes maximum

    # #print("randomUserId is ", randomUserID)
    cursorDrivers = userCollection.find({constants.ACTIVE_STATE: constants.NO, constants.ALSO_DRIVER: constants.YES,
                                         constants.CURRENT_ZONE: userSourceZone})
    drivers = list(cursorDrivers)
    total_drivers = len(drivers)
    closest_driver_time = 10
    closest_driver_id = ""
    closest_flag = False
    #
    print("------------------------------------------------------------------------------------------------")
    print("Finding Closest Driver (From Same Zone)...Please wait...")
    driverMongoId = ""
    for i in range(0, total_drivers):
        # print(drivers[i])

        driver_location = drivers[i][constants.CURRENT_LOCATION]

        source_geocode, destination_gecode, distance, time_2_int = commons.google_Maps_time_distance(source,
                                                                                                     driver_location)
        # print(source_geocode)
        # print(destination_gecode)
        # print(distance)
        # print(time_2_int)
        # print("Time Found ", time_2_int)
        # print("-------------------------------------------------------")

        if time_2_int <= closest_driver_time and closest_flag == False:
            tripSeatCapacity = drivers[i][constants.SEAT_CAPACITY]
            driverMongoId = drivers[i][constants.MONGO_ID]
            closest_driver_time = time_2_int
            driver = {constants.ROLE: constants.DRIVER,
                      constants.USER_ID: drivers[i][constants.USER_ID],
                      constants.SEAT_CAPACITY: drivers[i][constants.SEAT_CAPACITY],
                      constants.ALSO_DRIVER: drivers[i][constants.ALSO_DRIVER],
                      constants.MONGO_ID: drivers[i][constants.MONGO_ID],
                      constants.CHATTY_SCORE: drivers[i][constants.CHATTY_SCORE],
                      constants.SECURITY_SCORE: drivers[i][constants.SECURITY_SCORE],
                      constants.PUNCTUALITY_SCORE: drivers[i][constants.PUNCTUALITY_SCORE],
                      constants.FRIENDLINESS_SCORE: drivers[i][constants.FRIENDLINESS_SCORE],
                      constants.COMFORTIBILITY_SCORE: drivers[i][constants.COMFORTIBILITY_SCORE],
                      constants.UTT: drivers[i][constants.UTT],
                      constants.CURRENT_ZONE: drivers[i][constants.CURRENT_ZONE],
                      constants.CURRENT_LOCATION: drivers[i][constants.CURRENT_LOCATION],
                      constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)
                      }
            # trip = driver
            # 1 min is closest, stop the loop...
            if closest_driver_time == 1:
                trip = {}
                # print(driver)
                closest_flag = True
                break

    # Add the closest driver to rider in the trip
    # trip = driver, first_rider
    requiredDrivers = requiredDrivers + 1
    print(driver, first_rider)
    print("---------------------------------------------------------------------------------------")
    print("Trip UTT: ", tripUTT)
    print("Trip Seat Capacity: ", tripSeatCapacity)
    print("Current Zone: ", userSourceZone)
    print("Distance From Driver to Broadcasting User: (mins)", closest_driver_time)

    # endTime = dt.datetime.now() + dt.timedelta(minutes=tripUTT)
    # while True:
    #   if dt.datetime.now() >= endTime:
    #     print("Running for ", tripUTT)
    #     break

    # Updating Driver Details

    # Finding Riders!!!!
    print("-------------------------------------------------------------------------------------")
    filledSeatCount = 0
    print("Finding/ Searching for More Riders...")
    # randomUserID = random.randrange(1, constants.TOTAL_USERS)
    # print("randomUserId is ", randomUserID)
    userCollection = db.ridersndrivers
    foundRiders = []
    cursor_newRiders = userCollection.find(
        {  # constants.USER_ID: randomUserID,
            constants.CURRENT_ZONE: userSourceZone,
            constants.ACTIVE_STATE: constants.NO,
            constants.BROADCASTING: constants.YES,
            constants.ALSO_DRIVER: constants.NO,
            constants.CHATTY_SCORE: tripChatty,
            constants.SECURITY_SCORE: tripSecurity,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility})
    foundRiders = list(cursor_newRiders)
    #print(foundRiders)
    filledSeatCount += len(foundRiders)

    if foundRiders != []:
        #print("******Found Riders with Exact Characteristics in Same Zone...")
        ""
        #print(foundRiders)

    # Trip Chatty Plus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found in the Same Zone with Exact Characteristics....")
        #print("Finding for Riders in the Same Zone with Chatty Plus 1...")
        userCollection = db.ridersndrivers
        chatUpdate = 0
        if tripChatty == 5:
            chatUpdate == tripChatty - 1
        else:
            chatUpdate = tripChatty + 1
        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: chatUpdate,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)

    #print("Trip Chatty plus1 Results")
    #print(foundRiders)

    # Chatty Minus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Chatty Minus 1...")
        userCollection = db.ridersndrivers
        chatUpdate = 0
        if tripChatty == 1:
            chatUpdate == tripChatty + 1
        else:
            chatUpdate = tripChatty - 1
        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: chatUpdate,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Chatty Minus 1 Results")
    #print(foundRiders)

    # Security Plus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Security Plus 1...")
        userCollection = db.ridersndrivers
        securityUpdate = 0
        if tripSecurity == 5:
            securityUpdate == tripSecurity - 1
        else:
            securityUpdate = tripSecurity + 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: securityUpdate,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Security plus1 Results")
    #print(foundRiders)

    # Trip Security Minus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Security Minus 1...")
        userCollection = db.ridersndrivers
        securityUpdate = 0
        if tripSecurity == 1:
            securityUpdate == tripSecurity + 1
        else:
            securityUpdate = tripSecurity - 1
        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: securityUpdate,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("TripSecurity minus 1 Results")
    #print(foundRiders)

    # Punctuality Plus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Punctuality Plus 1...")
        userCollection = db.ridersndrivers
        punctualityUpdate = 0
        if tripPunctuality == 5:
            punctualityUpdate == tripPunctuality - 1
        else:
            punctualityUpdate = tripPunctuality + 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: punctualityUpdate,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
   # print("Trip Punctuality plus1 Results")
   # print(foundRiders)

    # Punctuality Minus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Punctuality Minus 1...")
        userCollection = db.ridersndrivers
        punctualityUpdate = 0
        if tripPunctuality == 1:
            punctualityUpdate == tripPunctuality + 1
        else:
            punctualityUpdate = tripPunctuality - 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: punctualityUpdate,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Punctuality Minus 1 Results")
    #print(foundRiders)

    # Friendliness Plus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Friendliness Plus 1...")
        userCollection = db.ridersndrivers
        friendlinessUpdate = 0
        if tripFriendliness == 5:
            friendlinessUpdate == tripFriendliness - 1
        else:
            friendlinessUpdate == tripFriendliness + 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: friendlinessUpdate,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Friendliness Plus 1 Results")
    #print(foundRiders)

    # Friendliness Minus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Friendliness Minus 1...")
        userCollection = db.ridersndrivers
        friendlinessUpdate = 0
        if tripFriendliness == 1:
            friendlinessUpdate == tripFriendliness + 1
        else:
            friendlinessUpdate == tripFriendliness - 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: friendlinessUpdate,
                constants.COMFORTIBILITY_SCORE: tripComfortibility,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Friendliness Minus 1 Results")
    #print(foundRiders)

    # Comfortibility Plus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Comfortibility Plus 1...")
        userCollection = db.ridersndrivers
        comfortUpdate = 0
        if tripComfortibility == 5:
            comfortUpdate == tripComfortibility - 1
        else:
            comfortUpdate == tripComfortibility + 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: comfortUpdate,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Comfortibility Plus 1 Results")
    #print(foundRiders)

    # Comfortibility Minus 1
    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found....")
        #print("Finding for Riders in the Same Zone with Comfortibility Minus 1...")
        userCollection = db.ridersndrivers
        comfortUpdate = 0
        if tripComfortibility == 1:
            comfortUpdate == tripComfortibility + 1
        else:
            comfortUpdate == tripComfortibility - 1

        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SECURITY_SCORE: tripSecurity,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: comfortUpdate,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print("Trip Comfortibility Minus 1 Results")
    #print(foundRiders)
   # print("Seat Count Now Is: ", filledSeatCount)

    for i in range(1, 6):
        if foundRiders == [] or filledSeatCount <= forriders:
            #print("No Riders Found in the Same Zone with Altered Characteristics....")
            #print("Completely Randomizing the Charcteristics")
            chatRandom = commons.altered_characteristics(tripChatty)
            secureRandom = commons.altered_characteristics(tripSecurity)
            punctualRandom = commons.altered_characteristics(tripPunctuality)
            friendRandom = commons.altered_characteristics(tripFriendliness)
            comfortRandom = commons.altered_characteristics(tripComfortibility)
            userCollection = db.ridersndrivers
            cursor_newRiders = userCollection.find(
                {  # constants.USER_ID: randomUserID,
                    constants.CURRENT_ZONE: userSourceZone,
                    constants.ACTIVE_STATE: constants.NO,
                    constants.BROADCASTING: constants.YES,
                    constants.ALSO_DRIVER: constants.NO,
                    constants.CHATTY_SCORE: chatRandom,
                    constants.SECURITY_SCORE: secureRandom,
                    constants.PUNCTUALITY_SCORE: punctualRandom,
                    constants.FRIENDLINESS_SCORE: friendRandom,
                    constants.COMFORTIBILITY_SCORE: comfortRandom,
                })
            foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)


    exact_close_match = filledSeatCount
    print("Exact Found Rider Count ", exact_close_match)

    if foundRiders == [] or filledSeatCount <= forriders:
        #print("No Riders Found in the Same Zone with Altered Characteristics....")
        #print("Finding Riders who are Currently Broadcasting irrespective of Characteristics...")
        userCollection = db.ridersndrivers
        cursor_newRiders = userCollection.find(
            {  # constants.USER_ID: randomUserID,
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                # constants.CHATTY_SCORE: chatRandom,
                # constants.SECURITY_SCORE: secureRandom,
                # constants.PUNCTUALITY_SCORE: punctualRandom,
                # constants.FRIENDLINESS_SCORE: friendRandom,
                # constants.COMFORTIBILITY_SCORE: comfortRandom,
            })
        foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    #print(foundRiders)

    if foundRiders == [] or filledSeatCount <= tripSeatCapacity:
        #print("No Broadcasting Riders Found in the Same Zone.")
        #print("Using Cloud Servers Now...")
        #print("Searching Riders in Other Zones...")
        commons.animation()
        while foundRiders == [] or filledSeatCount <= tripSeatCapacity:
            # print("Founding Riders from Other Zones...")
            # randomUserID = random.randrange(1, constants.TOTAL_USERS)
            # randomSourceZone = random.randrange(1, constants.TOTAL_ZONES)
            # print("randomUserId is ", randomUserID)
            userCollection = db.ridersndrivers
            cursor = userCollection.find(
                {  # constants.USER_ID: randomUserID,
                    # constants.CURRENT_ZONE: randomSourceZone,
                    constants.ACTIVE_STATE: constants.NO,
                    constants.BROADCASTING: constants.YES,
                    constants.ALSO_DRIVER: constants.NO,
                    constants.CHATTY_SCORE: tripChatty,
                    constants.SECURITY_SCORE: tripSecurity,
                    constants.PUNCTUALITY_SCORE: tripPunctuality,
                    constants.FRIENDLINESS_SCORE: tripFriendliness,
                    constants.COMFORTIBILITY_SCORE: tripComfortibility})
            # Generate a location from the zone
            foundRiders = list(cursor)
    filledSeatCount += len(foundRiders)
    #print(foundRiders)

    # print("--------------------------------------------")
    # print("Trip Details:")
    # print("Trip Seat Capacity: ", tripSeatCapacity)
    # print("Trip Total Distance: ", total_trip_distance)
    # print("Trip Total Time: ", total_time_2_int)
    # print("Trip UTT: ", tripUTT)
    # print("Total Trip Time: ", time_2_int+tripUTT)
    # print("Source Zone: ", userSourceZone)
    # print("Seat Count in Total", filledSeatCount)
    # print(trip)
    lastZone = 0
    print("--------------------------------------------")
    print("Working on Found Riders....")
    seatCount = 1
    for i in range(0, len(foundRiders)):
        ridersMatching = ridersMatching + 1
        # print("-------------------------------------------------------------------------")
        if seatCount <= tripSeatCapacity - 2:
            # newRiderId = foundRiders[i][constants.USER_ID]
            newRiderMongoId = foundRiders[i][constants.MONGO_ID]
            # newRiderChattyScore = foundRiders[i][constants.CHATTY_SCORE]
            # newRiderSecurityScore = foundRiders[i][constants.SECURITY_SCORE]
            # newRiderPunctualityScore = foundRiders[i][constants.PUNCTUALITY_SCORE]
            # newRiderFriendlinessScore = foundRiders[i][constants.FRIENDLINESS_SCORE]
            # newRiderComfortibilityScore = foundRiders[i][constants.COMFORTIBILITY_SCORE]
            # newRiderAlsoDriver = foundRiders[i][constants.ALSO_DRIVER]
            # newRiderCurrentZone = foundRiders[i][constants.CURRENT_ZONE]
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
                # print("Source is Close....Checking for Destinations Now...")
                if new_user_time_dest <= tripUTT:
                    userIDQueue.append(newRiderMongoId)
                    seatCount += 1
                    print("**********Source, Destination UTT Satisfied....User Accepted**************")
                    ridersMatched = ridersMatched + 1
                    print("Total Car Capacity: ", tripSeatCapacity)
                    print("Total Seats Filled: ", seatCount)
                    riders = {constants.ROLE: constants.RIDER,
                              constants.USER_ID: foundRiders[i][constants.USER_ID],
                              # constants.SEAT_CAPACITY: cursorRandomUser[0][constants.SEAT_CAPACITY],
                              constants.ALSO_DRIVER: foundRiders[i][constants.ALSO_DRIVER],
                              constants.MONGO_ID: foundRiders[i][constants.MONGO_ID],
                              constants.CHATTY_SCORE: foundRiders[i][constants.CHATTY_SCORE],
                              constants.SECURITY_SCORE: foundRiders[i][constants.SECURITY_SCORE],
                              constants.PUNCTUALITY_SCORE: foundRiders[i][constants.PUNCTUALITY_SCORE],
                              constants.FRIENDLINESS_SCORE: foundRiders[i][constants.FRIENDLINESS_SCORE],
                              constants.COMFORTIBILITY_SCORE: foundRiders[i][constants.COMFORTIBILITY_SCORE],
                              constants.UTT: foundRiders[i][constants.UTT],
                              constants.SOURCE: random_new_user_source,
                              constants.DESTINATION: random_new_user_destination,
                              constants.SOURCE_ADDRESS: destination_geocode_source,
                              constants.DEST_ADDRESS: destination_geocode_dest,
                              constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}
                    riders = riders, riders
                    # tripUTT = tripUTT - new_user_time_source
                    print("Trip UTT Reduced or Updated to minimal: ", tripUTT)
                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
                    userCollection.find_one_and_update({constants.MONGO_ID: newRiderMongoId},
                                                       {"$set": {constants.BROADCASTING: constants.NO}})
                    locationlist.append(random_new_user_source)
                    locationlist.append(random_new_user_destination)
                else:
                    # print("Destination too far...User not Accepted")
                    ""
            else:
                # print("Source UTT Not Satisfied....User Not Accepted")
                ""
        else:
            break

    # if seatCount < tripSeatCapacity-1:
    #     foundRiders = findingRiders.findRiders(userSourceZone, tripSeatCapacity, tripChatty, tripSecurity, tripPunctuality, tripFriendliness, tripComfortibility )
    #     print(foundRiders)

    print("--------Printing the Final Trip-------")
    print("Seat Left to be filled (Number of Poolers Not Found): ", (tripSeatCapacity - (seatCount + 1)))
    # print(trip)
    # print("Active User IDs: ", userIDQueue)

    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})

    # print("Starting Trip...")
    # commons.animation(60)
    # print("Processing with Trip (Picking Up Riders And Completing Trip Now...)")
    # commons.animation(60)
    # print("...Trip Finished... Making Driver Available and Riders Inactive")

    # Update Driver's Active State
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.NO}})
    driverNewLocationStatus = random.random()

    driverNewCurrentLocation = ""
    if driverNewLocationStatus <= 0.5:
        lastZone = userSourceZone
    else:
        ""
    driver_new_location = commons.generate_location(lastZone)
    # Update Driver Zone as Last Zone
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_ZONE: lastZone}})
    # Update Driver Location as Last User's Location
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_LOCATION: driver_new_location}})
    commons.updateNoBroadcast(userIDQueue)
    commons.updateNoActiveState(userIDQueue)

    # totalDistanceTime = commons.multiCoordinatesString(locationlist)
    # print(totalDistanceTime)
    # source_geocode_dest, destination_geocode_dest, new_user_distance_dest, new_user_time_dest = commons.google_Maps_time_distance(
    # source, totalDistanceTime)

    poolCompleted = ""
    if seatCount == tripSeatCapacity - 1:
        poolCompleted = constants.YES
    else:
        poolCompleted = constants.NO

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time_actual = datetime.now()

    time_secs, time_mins = commons.time_diff(start_time_actual, end_time_actual)

    if exact_close_match > seatCount:
        different_char_match = seatCount-1
    else:
        different_char_match = seatCount - exact_close_match



    print("--------------------------------To Be Inserted in Document----------------------------------")
    tripData = {
        "exact_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        constants.UTT: [parameterUTT, tripUTT],
        # total_trip_time": total_trip_time,
        # "total_trip_distance": total_trip_distance,
        "pool_completed": poolCompleted,
        "driverId": driverMongoId,
        "user_Q": userIDQueue,
        constants.TOTAL_RIDERS_CHECKED: ridersMatching,
        constants.TOTAL_RIDERS_MATCHED: ridersMatched,
        constants.TOTAL_DRIVERS: requiredDrivers,
        constants.TRIP_START_TIME: start_time,
        constants.TRIP_END_TIME: end_time,
        constants.TRIP_DIFF_SECS: time_secs,
        constants.TRIP_DIFF_MINS: time_mins
    }

    trip = {
        "tripData": tripData,
        "tripDriver": driver,
        "broadcasting_rider": first_rider,
        "otherRiders": riders
    }
    print(trip)
    print(constants.SEAT_CAPACITY, ":", tripSeatCapacity)
    print("seats_filled:", seatCount)
    print(constants.UTT, ":", parameterUTT, tripUTT)
    # total_trip_time": total_trip_time,
    # "total_trip_distance": total_trip_distance,
    print("pool_completed: ", poolCompleted)
    print(constants.TOTAL_RIDERS_CHECKED, ":", ridersMatching)
    print(constants.TOTAL_RIDERS_MATCHED, ":", ridersMatched)
    print(constants.TOTAL_DRIVERS, ":", requiredDrivers)
    print(constants.TRIP_START_TIME, ":", start_time)
    print(constants.TRIP_END_TIME, ":", end_time)
    print(constants.TRIP_DIFF_SECS, ":", time_secs)
    print(constants.TRIP_DIFF_MINS, ":", time_mins)

    tripCollectionDocs = db.tripCollection
    trip_id = tripCollectionDocs.insert_one(trip)
    print("Objects in trip", len(trip))

    return ridersMatching, ridersMatched, requiredDrivers, exact_close_match, different_char_match


