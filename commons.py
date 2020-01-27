import random
import constants
from dbconnection import db
import requests
import json
import time
import sys
from datetime import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getTimeStamp():
    return datetime.now().strftime(constants.TIME_STRING)


#Geneate a Specified Location
def generate_location(sourceZone):
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    # print(s_coordinates_str)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates

#Generate a Random Location from Random Zone
def generate_random_location():
    sourceZone = random.randrange(1, 263)
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    # print(s_coordinates_str)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates

def generate_random_location_with_Zone():
    sourceZone = random.randrange(1, 263)
    locations = db.zonenlocations
    s_cursor = locations.find({constants.ZONE_ID: sourceZone})
    s_list = list(s_cursor)
    while s_list == []:
        sourceZone = random.randrange(1, constants.TOTAL_ZONES)
        s_cursor = locations.find({constants.ZONE_ID: sourceZone})
        s_list = list(s_cursor)
    s_count = s_list[0][constants.LOCATION_COUNT]
    random_source_location_index = random.randrange(2, s_count - 2)
    cursor2 = locations.find({constants.ZONE_ID: sourceZone},
                             {constants.COORDINATES: {"$slice": [random_source_location_index, 1]}})
    s_coordinates = list(cursor2)
    s_coordinates_l = s_coordinates[0][constants.COORDINATES]
    s_coordinates_str = str(s_coordinates_l)
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates, sourceZone


def google_Maps_time_distance(source, destination):
    URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + source + "&destinations=" + destination + "&key=" + constants.MAP_KEY
    # print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
    }
    r = requests.get(URL, headers=headers)
    rdata = json.loads(r.text)
    #print(rdata)
    status = rdata["rows"][0]["elements"][0]["status"]
    if status == constants.ZERO_RESULTS:
        source_geocode = "Cannot Geocode Source"
        destination_geocode = "Cannot Geocode Destination"
        total_trip_distance = "1000 mi"
        total_time_2_int = 10000
    else:
        destination_geocode = rdata["destination_addresses"][0]
        source_geocode = rdata["origin_addresses"][0]
        total_trip_distance = rdata["rows"][0]["elements"][0]["distance"]["text"]
        total_trip_time = rdata["rows"][0]["elements"][0]["duration"]["text"]
        #print("Source Address = ", source_geocode)
        #print("Destination Address=", destination_gecode)
        #print("Total Trip Distance (miles) = ", total_trip_distance)
        #print("Total Trip Time Calculated(mins) = ", total_trip_time)
        total_trip_time.split(" ")
        total_trip_time_s1 = total_trip_time[0]
        total_trip_time_s2 = total_trip_time[1]
        total_trip_time_int = total_trip_time_s1 + total_trip_time_s2
        if total_trip_time_s2 == " ":
            total_trip_time_int = "0" + total_trip_time_s1
        total_time_2_int = int(total_trip_time_int)
    return source_geocode, destination_geocode, total_trip_distance, total_time_2_int


def altered_characteristics(tripNo):
    randomChar = random.random()
    if randomChar>0.7:
        randomChar = tripNo + 1
        if randomChar>5:
            randomChar = tripNo - 2
    else:
        randomChar = tripNo - 1
        if randomChar<1:
            randomChar = tripNo + 2
    return randomChar

def animation(no):
    animation = "|/-\\"
    for i in range(no):
        time.sleep(0.1)
        sys.stdout.write("Finding riders/drivers... Please Wait...\r" + animation[i % len(animation)])
        sys.stdout.flush()
        # do something
    #print("...Driver Located")

def updateNoBroadcast(userQ):
    userCollection = db.ridersndrivers
    for i in range(0, len(userQ)):
        userCollection.find_one_and_update({constants.MONGO_ID: userQ[i]},
                                           {"$set": {constants.BROADCASTING: constants.NO}})

def updateNoActiveState(userQ):
    userCollection = db.ridersndrivers
    for j in range(0, len(userQ)):
        userCollection.find_one_and_update({constants.MONGO_ID: userQ[j]},
                                           {"$set": {constants.ACTIVE_STATE: constants.NO}})


def removeLocationQuotes(s_coordinates_str):
    s_coordinates_str = s_coordinates_str.split(",")
    long = s_coordinates_str[0].replace("[", '')
    s_long = long.replace("'", "")
    lat = s_coordinates_str[1].replace("]", "")
    s_lat = lat.replace("'", "")
    coordinates = s_lat + "," + s_long
    return coordinates

def multiCoordinatesString(locationlist):
    strLoc = ""
    locDistTimeString = ""
    for i in range(0, len(locationlist)):
        strLoc = locationlist[i].replace(" ", "")
        strLoc = strLoc.replace(",", "%2C")
        if i == (len(locationlist) - 1):
            locDistTimeString = locDistTimeString + strLoc
        else:
            locDistTimeString = locDistTimeString + strLoc + "%7C"

    return locDistTimeString


def time_diff(start, end):
    distance = (end - start).total_seconds()
    #print(distance)
    mins = distance / 60
    str_mins = str(mins)
    str_mins = round(mins, 2)
    return distance, str_mins

def cursorRiders(userSourceZone, scoreList, zoneStat, parameterUTT):
    #Same Zone
    #Alternative Riders
    ridersCollection = db.ridersndrivers
    foundRiders = []

    if scoreList == 0:
        ""
    else:

        tripChatty = scoreList[0]
        tripSafety = scoreList[1]
        tripPunctuality = scoreList[2]
        tripFriendliness = scoreList[3]
        tripComfortibility = scoreList[4]

    #Find Broadcasting Rider
    if zoneStat == constants.JUST_UTT:
        randomUserID = random.randrange(1, constants.TOTAL_USERS)
        cursor = ridersCollection.find({
            constants.USER_ID: randomUserID,
            constants.ACTIVE_STATE: constants.NO,
            constants.ALSO_DRIVER: constants.NO,
            constants.BROADCASTING: constants.YES,
            constants.UTT: parameterUTT})
    #Find Driver
    elif zoneStat == constants.FIND_DRIVER:
        cursor = ridersCollection.find({
            constants.ACTIVE_STATE: constants.NO,
            constants.ALSO_DRIVER: constants.YES,
            constants.CURRENT_ZONE: userSourceZone})
    #User Source Zone and Exact, Altered Characteristics\
    elif zoneStat == constants.SZEC:
        cursor = ridersCollection.find(
            {#constants.USER_ID: randomUserID,
            constants.CURRENT_ZONE: userSourceZone,
            constants.ACTIVE_STATE: constants.NO,
            constants.BROADCASTING: constants.YES,
            constants.ALSO_DRIVER: constants.NO,
            constants.CHATTY_SCORE: tripChatty,
            constants.SAFETY_SCORE: tripSafety,
            constants.PUNCTUALITY_SCORE: tripPunctuality,
            constants.FRIENDLINESS_SCORE: tripFriendliness,
            constants.COMFORTIBILITY_SCORE: tripComfortibility})
    elif zoneStat == constants.ALL_BROADCASTING:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
            })
    elif zoneStat == constants.OTHER_ZONE:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.CHATTY_SCORE: tripChatty,
                constants.SAFETY_SCORE: tripSafety,
                constants.PUNCTUALITY_SCORE: tripPunctuality,
                constants.FRIENDLINESS_SCORE: tripFriendliness,
                constants.COMFORTIBILITY_SCORE: tripComfortibility})

    return cursor

def getChar():
    return [random.randrange(2, 6), random.randrange(2, 6), random.randrange(2, 6), random.randrange(2, 6), random.randrange(2, 6)]

def getChar_Extend_V2():
    return [random.randrange(0, 6), random.randrange(0, 6), random.randrange(0, 6), random.randrange(0, 6), random.randrange(0, 6)]

def getChar_Extended():
    charNo = []
    for i in range(1, 6):
        randomNp = random.random()
        if randomNp > 0.7:
            no = random.randrange(1, 6)
        else:
            no = 0
        charNo.append(no)
    return charNo

def returnDict(charArray):
    dictOut = {constants.CHATTY_SCORE: charArray[0], constants.SAFETY_SCORE: charArray[1], constants.PUNCTUALITY_SCORE: charArray[2],
               constants.FRIENDLINESS_SCORE: charArray[3], constants.COMFORTIBILITY_SCORE: charArray[4]}
    return dictOut

def avg_wait_time_for_trip(trip):
    wait_time = trip['broadcasting_rider'][constants.USER_WAIT_TIME_MINS]
    tripRiderCount = len(trip['otherRiders'])
    for i in range(1, tripRiderCount):
        time_m = trip['otherRiders'][i][constants.USER_WAIT_TIME_MINS]
        wait_time += time_m
    usercount = tripRiderCount + 1
    avg_time = wait_time / usercount
    return avg_time, wait_time, usercount

def vectorDistance(scoreDict1, scoreDict2):
    data = [
        scoreDict1, scoreDict2
    ]
    vec = DictVectorizer()
    matrix = vec.fit_transform(data).toarray()
    similarity_scores = cosine_similarity(matrix)
    matching_score = similarity_scores[0, 1]
    return matching_score

def vectorDistanceEnhanced(data):

    vec = DictVectorizer()
    matrix = vec.fit_transform(data)
    #print(matrix.toarray())
    similarity_scores = cosine_similarity(matrix)
    #print(similarity_scores)
    rider_index = []
    #matching_score = similarity_scores[0, 1]
    #print("Printing the  similarity")
    for i in range(1, len(similarity_scores)):
        #print(similarity_scores[0, i])
        if similarity_scores[0, i] > 0.85:
            #print("ith rider 85% more is ", i)
            rider_index.append(i)
    return rider_index

#Classifier with values 5,4,3
def cursorRidersMachineLearn(userSourceZone, char_dict, reg_classifier, max_score, same_or_other):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: max_score
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: max_score
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        #print(foundRiders[i])
        other_charDict = foundRiders[i][constants.CHAR_DICT]
        similarity_score = vectorDistance(char_dict, other_charDict)
        if similarity_score >= 0.85:
            #print("Found 85% match")
            #print("")
            riders.append(foundRiders[i])
    #print("For Classifier", reg_classifier, " with max score, ", max_score)
    #print(riders)
    return riders, filledSeatCount

#Classifier with values 5,4,3
def cursorRidersMachineLearnEnhanced(userSourceZone, char_dict, reg_classifier, max_score, same_or_other):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: max_score
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                reg_classifier: max_score
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index) - 1):
            riders.append(foundRiders[riders_index[i]])
        #print("Found ", len(riders), "Riders With Char 85% or more Match...Checking for UTT Matching")
    return riders, filledSeatCount


#Exact Classifier
def cursorRidersMachineLearnClassifier(userSourceZone, char_dict, reg_classifier, same_or_other):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        #print(foundRiders[i])
        other_charDict = foundRiders[i][constants.CHAR_DICT]
        similarity_score = vectorDistance(char_dict, other_charDict)
        if similarity_score >= 0.85:
            #print("Found 85% match")
            #print("")
            riders.append(foundRiders[i])
    #print("Riders Found From Cluster Calssifier in Same Zone", reg_classifier)
   #print(riders)
    return riders, filledSeatCount

#Exact Classifier
def cursorRidersMachineLearnClassifierEnhanced(userSourceZone, char_dict, reg_classifier, same_or_other):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.REG_CLASSIFIER: reg_classifier
            })
    foundRiders = list(cursor)
    #print(foundRiders)
    filledSeatCount = len(foundRiders)
    #print(filledSeatCount, "riders found")
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    #print("Data Dict")
    #print(data)
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index)-1):
            #print(riders_index[i])
            riders.append(foundRiders[riders_index[i]])
        #print("Found ", len(riders), "Riders With Char 85% or more Match...Checking for UTT Matching")
    #print("Riders Found From Cluster Calssifier in Same Zone", reg_classifier)
    #print("Enhanced riders are ", riders)
    return riders, filledSeatCount

def update_feedback_status(userIdQ):
    for i in range(0, len(userIdQ)):
        #print(userIdQ[i])
        userCollection = db.ridersndrivers
        userCollection.find_one_and_update({constants.USER_ID: userIdQ[i]},
                                           {"$set": {constants.FEEDBACK_GIVEN: constants.YES}})
    return None


def get_classifier(chatty, safety, punctuality, friendliness, comfortibility ):
    charDict = {constants.CHATTY_SCORE: chatty,
                constants.SAFETY_SCORE: safety,
                constants.PUNCTUALITY_SCORE: punctuality,
                constants.FRIENDLINESS_SCORE: friendliness,
                constants.COMFORTIBILITY_SCORE: comfortibility}
    classifier = max(charDict, key=charDict.get)
    classifier_regression_output = 0
    if classifier == constants.CHATTY_SCORE:
        classifier_regression_output = 1
    elif classifier == constants.SAFETY_SCORE:
        classifier_regression_output = 2
    elif classifier == constants.PUNCTUALITY_SCORE:
        classifier_regression_output = 3
    elif classifier == constants.FRIENDLINESS_SCORE:
        classifier_regression_output = 4
    elif classifier == constants.COMFORTIBILITY_SCORE:
        classifier_regression_output = 5
    return classifier, classifier_regression_output

def cursorFeedbackMachineLearnClassifierEnhanced(userSourceZone, char_dict, reg_classifier, same_or_other):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE:
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.FEEDBACK_CLASSIFIER: reg_classifier
            })
    else:
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.FEEDBACK_CLASSIFIER: reg_classifier
            })
    foundRiders = list(cursor)
    #print(foundRiders)
    filledSeatCount = len(foundRiders)
    #print(filledSeatCount, "riders found")
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    #print("Data Dict")
    #print(data)
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index)-1):
            #print(riders_index[i])
            riders.append(foundRiders[riders_index[i]])
        #print("Found ", len(riders), "Riders With Char 85% or more Match...Checking for UTT Matching")
    #print("Riders Found From Cluster Calssifier in Same Zone", reg_classifier)
    #print("Enhanced riders are ", riders)
    return riders, filledSeatCount


#Classifier with values 5,4,3
def givenClassifierBasedSearch(userSourceZone, char_dict, classifier_string, same_or_other, given):
    ridersCollection = db.ridersndrivers
    #print("Reg_Classifier is ", reg_classifier)
    riders = []
    data = []
    data.append(char_dict)
    if same_or_other == constants.SAME_ZONE and given == constants.YES:
        print("Searching with Same Feedback-Given-Classifier in Same Zone")
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GIVEN_FEEDBACK_CLASSIFIER: classifier_string

            })
    elif same_or_other == constants.SAME_ZONE and given == constants.NO:
        print("Searching with Riders Where Feedback-Given-Classifier = Feedback-Received-Classifier in Same Zone")
        cursor = ridersCollection.find(
            {
                constants.CURRENT_ZONE: userSourceZone,
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GOT_FEEDBACK_CLASSIFIER: classifier_string

            })
    elif same_or_other == constants.OTHER_ZONE and given == constants.YES :
        print("Searching with Same Feedback-Given-Classifier in Other Zones")
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GIVEN_FEEDBACK_CLASSIFIER: classifier_string
            })
    elif same_or_other == constants.OTHER_ZONE and given == constants.NO :
        print("Searching with Riders Where Feedback-Given-Classifier = Feedback-Received-Classifier in Other Zone")
        cursor = ridersCollection.find(
            {
                constants.ACTIVE_STATE: constants.NO,
                constants.BROADCASTING: constants.YES,
                constants.ALSO_DRIVER: constants.NO,
                constants.GOT_FEEDBACK_CLASSIFIER: classifier_string
            })
    foundRiders = list(cursor)
    filledSeatCount = len(foundRiders)
    for i in range(0, len(foundRiders)):
        data.append(foundRiders[i][constants.CHAR_DICT])
    riders_index = vectorDistanceEnhanced(data)
    if riders_index == [] or riders_index == "":
        riders = None
    else:
        for i in range(0, len(riders_index) - 1):
            riders.append(foundRiders[riders_index[i]])
        #print("Found ", len(riders), "Riders With Char 85% or more Match...Checking for UTT Matching")
    return riders, filledSeatCount