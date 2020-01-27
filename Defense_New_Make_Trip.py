from dbconnection import db
import random
import constants
from datetime import datetime
import commons
#import feedback_sys
import variance
import uttMatching
import fdbck_aggr
import fdbck_sys_2
import warnings
warnings.filterwarnings("ignore")


def mainResults(parameteruserId, parameterUTT):
    #trip_riders = {}
    #trip_id = ""
    #trip_mongoId = ""
    #avg_waiting_time = 0
    #user_wait_start_time = datetime.now()
    driverNo = 0
    ridersMatching = 0
    forRiders = 0
    ridersMatched = 1
    requiredDrivers = 0
    userIDQueue = []
    userNoQueue = []
    driver = {}
    #first_rider = {}
    riders = {}
    locationlist = []
    #data = []
    returnData = []
    #last_zone = 0
    start_time = datetime.now().strftime(constants.TIME_STRING)
    start_time_actual = datetime.now()
    broadcasting_rider_start_time = start_time_actual
    userCollection = db.ridersndrivers
    #userSourceZone, scoreList, zoneStat, parameterUTT
    #cursor = commons.cursorRiders(0, 0, constants.JUST_UTT, parameterUTT)

    cursorRandomUser = []

    # Finds Only Inactive and Broacasting Rider - A True Broadcasting Rider
    #while cursorRandomUser == []:
     #   randomUserID = random.randrange(1, constants.TOTAL_USERS)
    cursor = userCollection.find({
            constants.USER_ID: parameteruserId})
    cursorRandomUser = list(cursor)
    #print(cursorRandomUser)
    #print("Broadcasting Rider Found...")
    #print("Broadcasting Rider Details:", cursorRandomUser)
    tripUTT = cursorRandomUser[0][constants.UTT]
    Broadcasting_userId = cursorRandomUser[0][constants.MONGO_ID]
    Broadcasting_userNo = cursorRandomUser[0][constants.USER_ID]
    userIDQueue.append(Broadcasting_userId)
    userNoQueue.append(Broadcasting_userNo)
    #userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       #{"$set": {constants.ACTIVE_STATE: constants.YES}})
    #userCollection.find_one_and_update({constants.MONGO_ID: Broadcasting_userId},
                                       #{"$set": {constants.BROADCASTING: constants.NO}})
    userSourceZone = cursorRandomUser[0][constants.CURRENT_ZONE]
    userSourceLocation = cursorRandomUser[0][constants.CURRENT_LOCATION]
    tripSeatCapacity = 0
    tripChatty = cursorRandomUser[0][constants.CHATTY_SCORE]
    tripSafety = cursorRandomUser[0][constants.SAFETY_SCORE]
    tripPunctuality = cursorRandomUser[0][constants.PUNCTUALITY_SCORE]
    tripFriendliness = cursorRandomUser[0][constants.FRIENDLINESS_SCORE]
    tripComfortibility = cursorRandomUser[0][constants.COMFORTIBILITY_SCORE]
    charDict = cursorRandomUser[0][constants.CHAR_DICT]
    reg_classifier = cursorRandomUser[0][constants.REG_CLASSIFIER]
    feed_back_status = cursorRandomUser[0][constants.FEEDBACK_GIVEN]
    feedback_classifier = constants.NO
    #if feed_back_status == constants.YES:
     #   feedback_classifier = cursorRandomUser[0][constants.FEEDBACK_CLASSIFIER]

    source = commons.generate_location(userSourceZone)
    destination = commons.generate_random_location()
    locationlist.append(destination)

    #print("Printing User's Broadcasting Locations and Trip Details.....")
    # Using Google Map Apis
    source_geocode, destination_gecode, total_trip_distance, total_time_2_int = commons.google_Maps_time_distance(
        source, destination)

    # print(
    #     "------------------------------------THE ENHANCED RIDE SHARING MODEL------------------------------------------")
    # print("-------------------------RIDER DETAILS----------------------------------")
    # print("MongoId: ", Broadcasting_userId)
    # print("UserId: ", Broadcasting_userNo)
    # print("Trip Characteristics: ", cursorRandomUser[0]["char_dict"])
    # print("Trip UTT:", parameterUTT)
    # print("Broadcasting Rider Zone: ", userSourceZone)
    if feed_back_status == constants.YES:
        #print("User has Performed Trips Before. Therefore System will First Search Riders Based on Computed Classifier")
        feedback_given_classifer = cursorRandomUser[0]["giving_feedback_classifier"]
        feedback_got_classifer = cursorRandomUser[0]["got_feedback_classifier"]

        #print("Feedback-Given-Classifier: ", feedback_given_classifer)
       #print("Feedback-Received-Classifier: ", feedback_got_classifer)

    else:
        ""
        #print("This is the First Trip for User with UserId: ", Broadcasting_userNo)

    #print("--------------------------------------------------------------------------------------")
    # #print("randomUserId is ", randomUserID)
    cursorDrivers = commons.cursorRiders(userSourceZone, 0, constants.FIND_DRIVER, parameterUTT)
    drivers = list(cursorDrivers)
    total_drivers = len(drivers)
    closest_driver_time = 10
    closest_driver_id = ""
    closest_flag = False
    #
    #print("------------------------------------------------------------------------------------------------")
    #print("Searching for the Closest Driver from the Same Zone ", userSourceZone, "...")
    driverMongoId = ""
    for i in range(0, total_drivers):
        # print(drivers[i])

        driver_location = drivers[i][constants.CURRENT_LOCATION]

        source_geocode, destination_gecode, distance, time_2_int = commons.google_Maps_time_distance(source,
                                                                                                     driver_location)

        if time_2_int <= closest_driver_time and closest_flag is False:
            tripSeatCapacity = drivers[i][constants.SEAT_CAPACITY]
            driverMongoId = drivers[i][constants.MONGO_ID]
            driverNo = drivers[i][constants.USER_ID]
            closest_driver_time = time_2_int
            driver = {constants.ROLE: constants.DRIVER,
                      constants.USER_ID: drivers[i][constants.USER_ID],
                      constants.SEAT_CAPACITY: drivers[i][constants.SEAT_CAPACITY],
                      constants.ALSO_DRIVER: drivers[i][constants.ALSO_DRIVER],
                      constants.MONGO_ID: drivers[i][constants.MONGO_ID],
                      constants.CHATTY_SCORE: drivers[i][constants.CHATTY_SCORE],
                      constants.SAFETY_SCORE: drivers[i][constants.SAFETY_SCORE],
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

    broadcasting_rider_end_time = datetime.now()
    user_wait_start_time = broadcasting_rider_end_time
    broadcasting_time_secs, broadcasting_time_mins = commons.time_diff(broadcasting_rider_start_time,
                                                                       broadcasting_rider_end_time)

    first_rider = {constants.ROLE: constants.RIDER,
                   constants.USER_ID: cursorRandomUser[0][constants.USER_ID],
                   constants.CHAR_DICT: charDict,
                   constants.REG_CLASSIFIER: reg_classifier,
                   constants.FEEDBACK_CLASSIFIER: feedback_classifier,
                   constants.ALSO_DRIVER: cursorRandomUser[0][constants.ALSO_DRIVER],
                   constants.MONGO_ID: cursorRandomUser[0][constants.MONGO_ID],
                   constants.CHATTY_SCORE: cursorRandomUser[0][constants.CHATTY_SCORE],
                   constants.SAFETY_SCORE: cursorRandomUser[0][constants.SAFETY_SCORE],
                   constants.PUNCTUALITY_SCORE: cursorRandomUser[0][constants.PUNCTUALITY_SCORE],
                   constants.FRIENDLINESS_SCORE: cursorRandomUser[0][constants.FRIENDLINESS_SCORE],
                   constants.COMFORTIBILITY_SCORE: cursorRandomUser[0][constants.COMFORTIBILITY_SCORE],
                   constants.UTT: cursorRandomUser[0][constants.UTT],
                   constants.SOURCE: source,
                   constants.DESTINATION: destination,
                   constants.SOURCE_ADDRESS: source_geocode,
                   constants.DEST_ADDRESS: destination_gecode,
                   constants.USER_WAIT_TIME_SECS: broadcasting_time_secs,
                   constants.USER_WAIT_TIME_MINS: broadcasting_time_mins,
                   constants.CURRENT_TIME: datetime.now().strftime(constants.TIME_STRING)}
    #print("Broadcasting rider details")
    #print(first_rider)
    # #Search Drivers in 2 minutes maximum


    # Add the closest driver to rider in the trip
    # trip = driver, first_rider
    requiredDrivers = requiredDrivers + 1

    #print("----------------------------Selected Driver Details-----------------------------------")
    #print("Driver Alloted to Broadcasting Rider")
    #rint(driver, first_rider)
    #print("Trip UTT: ", tripUTT)
    #print("Driver Car Seating Capacity: ", tripSeatCapacity)
    #print("Driver found in Zone: ", userSourceZone)
    #print("Trip UTT = ", tripUTT)
    #print("Total Trip Time with UTT = ", total_time_2_int + tripUTT)
    #print("Distance From Driver to Broadcasting User (mins): ", closest_driver_time)


    # endTime = dt.datetime.now() + dt.timedelta(minutes=tripUTT)
    # while True:
    #   if dt.datetime.now() >= endTime:
    #     print("Running for ", tripUTT)
    #     break

    # Updating Driver Details

    # Finding Riders!!!!

    #print("-------------------------------------------------------------------------------------")
    filledSeatCount = 0
    lastZone = random.randrange(2, constants.TOTAL_ZONES)
    seatCount = 1
    #print("Finding/ Searching for Riders...")
    #print("----------------------------------EXACT SEARCH---------------------------------------")
    userCollection = db.ridersndrivers
    user_wait_start_time = datetime.now()
    # Exact Similar Characteristics
    char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
    cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
    foundRiders = list(cursor_newRiders)
    filledSeatCount += len(foundRiders)
    if filledSeatCount != 0:
        data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone, source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
        returnData = uttMatching.UTTMatching(data)
    if returnData == None or returnData == []:
        ""
        #print("No Current Active or Broadcasting Riders Found By Exact Match")
    else:
        #print("Found Riders by Exact Char Match & UTT Match....")
        riders = returnData[0]
        tripUTT = returnData[1]
        userIDQueue = returnData[2]
        locationlist = returnData[3]
        ridersMatching = returnData[4]
        ridersMatched = returnData[5]
        lastZone = returnData[6]
        seatCount = returnData[7]
        user_wait_start_time = returnData[8]
        userNoQueue = returnData[9]
        forRiders += ridersMatching

    '''
    # Trip Chatty Plus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        chatUpdate = 0
        if tripChatty == 5:
            chatUpdate = tripChatty - 1
        else:
            chatUpdate = tripChatty + 1

        char = [chatUpdate, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Chatt+1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Chatty Minus 1

    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        chatUpdate = 0
        if tripChatty == 1:
            chatUpdate = tripChatty + 1
        else:
            chatUpdate = tripChatty - 1

        char = [chatUpdate, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Chatt-1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Safety Plus 1

    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        safetyUpdate = 0
        if tripSafety == 5:
            safetyUpdate = tripSafety - 1
        else:
            safetyUpdate = tripSafety + 1

        char = [tripChatty, safetyUpdate, tripPunctuality, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Safety+1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Safety Minus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        safetyUpdate = 0
        if tripSafety == 1:
            safetyUpdate = tripSafety + 1
        else:
            safetyUpdate = tripSafety - 1

        char = [tripChatty, safetyUpdate, tripPunctuality, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Safety-1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Punctuality Plus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        punctualityUpdate = 0
        if tripPunctuality == 5:
            punctualityUpdate == tripPunctuality - 1
        else:
            punctualityUpdate = tripPunctuality + 1

        char = [tripChatty, tripSafety, punctualityUpdate, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Punctuality+1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Punctuality Minus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        punctualityUpdate = 0
        if tripPunctuality == 1:
            punctualityUpdate == tripPunctuality + 1
        else:
            punctualityUpdate = tripPunctuality - 1

        char = [tripChatty, tripSafety, punctualityUpdate, tripFriendliness, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Punctuality-1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Friendliness Plus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        friendlinessUpdate = 0
        if tripFriendliness == 5:
            friendlinessUpdate == tripFriendliness - 1
        else:
            friendlinessUpdate == tripFriendliness + 1

        char = [tripChatty, tripSafety, tripPunctuality, friendlinessUpdate, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Friendliness+1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Friendliness Minus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        friendlinessUpdate = 0
        if tripFriendliness == 1:
            friendlinessUpdate == tripFriendliness + 1
        else:
            friendlinessUpdate == tripFriendliness - 1

        char = [tripChatty, tripSafety, tripPunctuality, friendlinessUpdate, tripComfortibility]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Friendliness-1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Trip Comfortibility Plus 1
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        comfortUpdate = 0
        if tripComfortibility == 5:
            comfortUpdate == tripComfortibility - 1
        else:
            comfortUpdate == tripComfortibility + 1

        char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, comfortUpdate]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Comfort+1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Comfortibility Minus 1

    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        comfortUpdate = 0
        if tripComfortibility == 1:
            comfortUpdate == tripComfortibility + 1
        else:
            comfortUpdate == tripComfortibility - 1

        char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, comfortUpdate]
        cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.SZEC, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            print("Comfort-1 & UTT Match....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching
    '''
    if feed_back_status == constants.YES:
        #print("")
        #print("---------------------FEEDBACK-GIVEN-CLASSIFIER SEARCH--------------------------------")
        #Feedback-Given-Classifier Search
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = commons.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                                 feedback_given_classifer,
                                                                                                 constants.SAME_ZONE,
                                                                                                 given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
               #print("No Riders Found with Same Feedback-Given-Classifier")
            else:
                #print("Riders are Found Having Same Feedback-Given-Classifier....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
        #print("")
        #print("---------------------FEEDBACK-RECEIVED-CLASSIFIER SEARCH--------------------------------")
        # Feedback-Received-Classifier Search
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = commons.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                           feedback_got_classifer,
                                                                                           constants.SAME_ZONE,
                                                                                           given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                #print("No Riders Found with Same Feedback-Given-Classifier")
            else:
                #print("Riders are Found Having Same Feedback-Given-Classifier....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching
    #print("")
    #print("-----------------------------CLOSER SEARCH--------------------------------------")
    for no in range(0, 4):
        # All Broadcasting Riders By Exact Register Classifier In Same Zone
        if seatCount <= (tripSeatCapacity-2):
            userCollection = db.ridersndrivers
            cursor_newRiders, filledSeatCountfunction = commons.cursorRidersMachineLearnClassifierEnhanced(userSourceZone, charDict, reg_classifier, constants.SAME_ZONE)
            filledSeatCount += filledSeatCountfunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
            else:
                #print(" Riders Found In Same Zone with Exact Registration Classifier....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching

        #All Broadcasting Riders With Register Classifier with Max Score 5 In Same Zone
        if seatCount <= (tripSeatCapacity-2):
            userCollection = db.ridersndrivers
            max_score = 5
            cursor_newRiders , filledSeatCountFunction= commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score,
                                                                constants.SAME_ZONE)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount, userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            #print(returnData)
            if returnData == None or returnData == []:
                ""
            else:
                #print("Riders Found in Same Zone with Registration Classifier Score 5....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching

        # All Broadcasting Driver With Register Classifier with Max Score 4 In Same Zone
        if seatCount <= (tripSeatCapacity-2):
            userCollection = db.ridersndrivers
            max_score = 4
            cursor_newRiders, filledSeatCountFunction = commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score, constants.SAME_ZONE)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
            else:
                #print("Riders Found in Same Zone with Registration Classifier Score 4....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching


        # All Broadcasting Driver With Register Classifier with Max Score 3 In Same Zone
        if seatCount <= (tripSeatCapacity-2):
            userCollection = db.ridersndrivers
            max_score = 3
            cursor_newRiders, filledSeatCountFunction = commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score, constants.SAME_ZONE)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                #error here
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
            else:
                #print("Riders Found In Same Zone with Registration Classifier Score 3....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching

        #Feedback Classifier Based Rider Search
        if seatCount <= (tripSeatCapacity-2) and feed_back_status == constants.YES:
            userCollection = db.ridersndrivers
            cursor_newRiders, filledSeatCountfunction = commons.cursorFeedbackMachineLearnClassifierEnhanced(userSourceZone, charDict, reg_classifier, constants.SAME_ZONE)
            filledSeatCount += filledSeatCountfunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            if returnData == None or returnData == []:
                ""
            else:
                #print(" Riders found are from Same Zone with Exact Registration Classifier....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching



    # All Broadcasting Riders By Classifier In Other Zone
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        cursor_newRiders, filledSeatCountfunction = commons.cursorRidersMachineLearnClassifierEnhanced(userSourceZone, charDict, reg_classifier,
                                                                      constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders Found are from Other Zone with Exact Classifier....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching


    #All Broadcasting Riders With Register Classifier with Max Score 5 In Other Zone

    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        max_score = 5
        cursor_newRiders, filledSeatCountFunction = commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score,
                                                            constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountFunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders Found are from Other Zone with Classifier Score 5....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # All Broadcasting Driver With Register Classifier with Max Score 4 In Other Zone
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        max_score = 4
        cursor_newRiders, filledSeatCountfunction = commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score, constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                    userSourceZone,
                    source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders Found are from Other Zone with Classifier Score 4....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # All Broadcasting Driver With Register Classifier with Max Score 3 In Other Zone
    if seatCount <= (tripSeatCapacity-2):
        userCollection = db.ridersndrivers
        max_score = 3
        cursor_newRiders, filledSeatCountfunction = commons.cursorRidersMachineLearnEnhanced(userSourceZone, charDict, reg_classifier, max_score,
                                                            constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders Found are from Other Zone with Classifier Score 3....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    #Feedback Based Classification.# All Broadcasting Riders By Classifier In Other Zone
    if seatCount <= (tripSeatCapacity-2) and feed_back_status == constants.YES:
        userCollection = db.ridersndrivers
        cursor_newRiders, filledSeatCountfunction = commons.cursorFeedbackMachineLearnClassifierEnhanced(userSourceZone, charDict, reg_classifier,
                                                                      constants.OTHER_ZONE)
        filledSeatCount += filledSeatCountfunction
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders Found are from Other Zone with Feedback Classifier....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    # Feedback-Given-Classifier Search Other Zones
    if feed_back_status == constants.YES:
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.YES
            cursor_newRiders, filledSeatCountFunction = commons.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                           feedback_given_classifer,
                                                                                           constants.OTHER_ZONE,
                                                                                           given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                #print("No Riders Found with Same Feedback-Given-Classifier Other Zones")
            else:
               #print("Riders are Found Having Same Feedback-Given-Classifier Other Zones....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching

        # Feedback-Received-Classifier Search All zones
        if seatCount <= (tripSeatCapacity - 2):
            userCollection = db.ridersndrivers
            max_score = 0
            given = constants.NO
            cursor_newRiders, filledSeatCountFunction = commons.givenClassifierBasedSearch(userSourceZone, charDict,
                                                                                           feedback_got_classifer,
                                                                                           constants.OTHER_ZONE,
                                                                                           given)
            filledSeatCount += filledSeatCountFunction
            if filledSeatCount != 0:
                data = [riders, tripUTT, ridersMatching, ridersMatched, cursor_newRiders, tripSeatCapacity, seatCount,
                        userSourceZone,
                        source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
                returnData = uttMatching.UTTMatching(data)
            # print(returnData)
            if returnData == None or returnData == []:
                ""
                #print("No Riders Found with Same Feedback-Received-Classifier in Other Zones")
            else:
                #print("Riders are Found Having Same Feedback-Received-Classifier in Other Zones....")
                riders = returnData[0]
                tripUTT = returnData[1]
                userIDQueue = returnData[2]
                locationlist = returnData[3]
                ridersMatching = returnData[4]
                ridersMatched = returnData[5]
                lastZone = returnData[6]
                seatCount = returnData[7]
                user_wait_start_time = returnData[8]
                userNoQueue = returnData[9]
                forRiders += ridersMatching

    exact_close_match = seatCount
    #print("Number of Matched by Exact or Closer Characteristics Matching", exact_close_match)


    #Same Zone All Broadcasting
    if seatCount <= (tripSeatCapacity-2):
        #print("---------------------ALTERNATIVE SEARCH--------------------------------")
        userCollection = db.ridersndrivers
        cursor_newRiders = commons.cursorRiders(userSourceZone, 0, constants.ALL_BROADCASTING, parameterUTT)
        foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        # print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders found are from Same Zone All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    #All Zones All Broadcasting
    if seatCount <= (tripSeatCapacity-2):
        while foundRiders == [] or filledSeatCount <= tripSeatCapacity:
            userCollection = db.ridersndrivers
            char = [tripChatty, tripSafety, tripPunctuality, tripFriendliness, tripComfortibility]
            cursor_newRiders = commons.cursorRiders(userSourceZone, char, constants.OTHER_ZONE, parameterUTT)
            foundRiders = list(cursor_newRiders)
        filledSeatCount += len(foundRiders)
        if filledSeatCount != 0:
            data = [riders, tripUTT, ridersMatching, ridersMatched, foundRiders, tripSeatCapacity, seatCount, userSourceZone,
                source, destination, userIDQueue, locationlist, user_wait_start_time, userNoQueue]
            returnData = uttMatching.UTTMatching(data)
        #print(returnData)
        if returnData == None or returnData == []:
            ""
        else:
            #print("Riders fund are from All Zones All Broadcasting....")
            riders = returnData[0]
            tripUTT = returnData[1]
            userIDQueue = returnData[2]
            locationlist = returnData[3]
            ridersMatching = returnData[4]
            ridersMatched = returnData[5]
            lastZone = returnData[6]
            seatCount = returnData[7]
            user_wait_start_time = returnData[8]
            userNoQueue = returnData[9]
            forRiders += ridersMatching

    #print("For rider matched are", forRiders)
    different_char_match = tripSeatCapacity - seatCount - 1
    #print("Differenct Char Broadcasting Count ", different_char_match)

    #print("Lcation List:", locationlist)
    #print("--------Printing the Final Trip-------")
    #print("Seat Left to be filled (Number of Poolers Not Found): ", (tripSeatCapacity - (seatCount + 1)))
    seats_not_filled = tripSeatCapacity - (seatCount + 1)
    # print(trip)
    # print("Active User IDs: ", userIDQueue)

    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.YES}})
    # Update Driver's Active State
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.ACTIVE_STATE: constants.NO}})
    driverNewLocationStatus = random.random()

    driverNewCurrentLocation = ""
    if driverNewLocationStatus <= 0.5:
        lastZone = userSourceZone

    driver_new_location = commons.generate_location(lastZone)
    # Update Driver Zone as Last Zone
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_ZONE: lastZone}})
    # Update Driver Location as Last User's Location
    userCollection.find_one_and_update({constants.MONGO_ID: driverMongoId},
                                       {"$set": {constants.CURRENT_LOCATION: driver_new_location}})
    commons.updateNoBroadcast(userIDQueue)
    commons.updateNoActiveState(userIDQueue)

    #totalDistanceTime = commons.multiCoordinatesString(locationlist)
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

    # if exact_close_match > seatCount:
    #     different_char_match = seatCount-1
    # else:
    #     different_char_match = seatCount - exact_close_match
    print("")
    #print("--------------------------------The Final Trip Document----------------------------------")
    tripData = {
        "pool_completed": poolCompleted,
        "exact_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        "seats_not_filled": seats_not_filled,
        constants.UTT: [parameterUTT, tripUTT],
        # total_trip_time": total_trip_time,
        # "total_trip_distance": total_trip_distance,
        "driverId": driverMongoId,
        "user_MongoQ": userIDQueue,
        "userQ": userNoQueue,
        constants.TOTAL_RIDERS_CHECKED: ridersMatching,
        constants.TOTAL_RIDERS_MATCHED: ridersMatched,
        constants.TOTAL_DRIVERS: requiredDrivers,
        constants.TRIP_START_TIME: start_time,
        constants.TRIP_END_TIME: end_time,
        constants.TRIP_DIFF_SECS: time_secs,
        constants.TRIP_DIFF_MINS: time_mins,
        "trip_characteristics": {
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility
        }
    }

    trip = {
        "tripData": tripData,
        "tripDriver": driver,
        "broadcasting_rider": first_rider,
        "otherRiders": riders
    }

    avg_time, wait_time, usercount = commons.avg_wait_time_for_trip(trip)
    avg_time = round(avg_time, 2)

    tripCollectionDocs = db.tripCollection
    trip_id = tripCollectionDocs.insert_one(trip)
    tripcursor = tripCollectionDocs.find().sort(constants.MONGO_ID, -1)
    listTrip = list(tripcursor)
    trip_mongoId = listTrip[0][constants.MONGO_ID]
    tripCollectionDocs.remove({constants.MONGO_ID: trip_mongoId})

    tripData = {
        constants.TRIP_MONGOID: trip_mongoId,
        "average_waiting_time": avg_time,
        "pool_completed": poolCompleted,
        "exact_match": exact_close_match,
        "different_match": different_char_match,
        constants.SEAT_CAPACITY: tripSeatCapacity,
        "seats_filled": seatCount,
        "seats_not_filled": seats_not_filled,
        constants.UTT: [parameterUTT, tripUTT],
        # total_trip_time": total_trip_time,
        # "total_trip_distance": total_trip_distance,
        "driverId": driverMongoId,
        "user_MongoQ": userIDQueue,
        "userQ": userNoQueue,
        constants.TOTAL_RIDERS_CHECKED: ridersMatching,
        constants.TOTAL_RIDERS_MATCHED: usercount,
        constants.TOTAL_DRIVERS: requiredDrivers,
        constants.TRIP_START_TIME: start_time,
        constants.TRIP_END_TIME: end_time,
        constants.TRIP_DIFF_SECS: time_secs,
        constants.TRIP_DIFF_MINS: time_mins,
        "trip_characteristics": {
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility
        }
    }
    #
    # print("Trip Characteristics: ", charDict)
    # print("Trip UTT (mins):", parameterUTT)
    # print("Vehicle Seating Capacity: ", tripSeatCapacity)
    # print("Number of Seats Filled: ", seatCount)
    # print("Number of Seats Not Filled", seats_not_filled)
    # print("Pool Completion Status: ", poolCompleted)
    # print("Trip Users: ", userNoQueue)
    # print("Number of Riders By Exact or Closer Matching: ", exact_close_match)
    # print("Number of Riders By Alternative Matching: ", tripSeatCapacity-exact_close_match)
    # print("Time Taken For Trip Formation (mins) :", time_mins)
    # print("Time Taken For Trip Formation (secs) :", time_secs)
    # print("Total User Waiting Time in the Trip (mins): ", avg_time)
    #
    # print("-----------------------------------------------------------------------------------------------")

    trip = {
        constants.TRIP_MONGOID: trip_mongoId,
        "tripData": tripData,
        "tripDriver": driver,
        "broadcasting_rider": first_rider,
        "otherRiders": riders
    }
    trip_id = tripCollectionDocs.insert_one(trip)
    #print(trip)

    #userIDQueue.append(driverMongoId)
    #userMongoQ, driverMongoQ, userIdQ, driverId, tripId

    if riders == {} or riders == None or riders == constants.EMPTY_STRING:
        ""
    else:
        fdbck_sys_2.basic_feedback(userIDQueue, driverMongoId, userNoQueue, driverNo, trip_mongoId)
        variance.variance_given_classifier(userNoQueue)
        variance.variance_got_classifier(userNoQueue)
    #variance.variance_got_classifier(userNoQueue)
    #fdbck_aggr.feedback_aggr(userNoQueue)


    return ridersMatching, usercount, requiredDrivers, exact_close_match, different_char_match, trip_mongoId, wait_time, usercount



#trip_UTT = int(input("Enter rider UTT (mins):"))
#print("System Is Searching for a Rider whose UTT is ", trip_UTT, "Minutes and Broadcasting Status is Yes")
#mainResults(trip_UTT, 1)
