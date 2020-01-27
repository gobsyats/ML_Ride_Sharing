#import matchingPhase2
#import matchingPhase3
#import matchingPhase4_fbClass
import matching_Phase5a
import commons
import constants
from dbconnection import db
from datetime import datetime

document_no = 0
strUTT = input("Enter UTT: ")
UTT = int(strUTT)
riderCheck = input("Enter Total No of Riders To Be Checked: ")
riderCheck_int = int(riderCheck)
trip_ids = []

start = 1
end = 5
for i in range(start, end):
    print("Running  ", end-1, " times")
    ridersMatchingCount = 0
    ridersMatchedCount = 0
    requiredDriversCount = 0
    totalRidersInPool = 0
    exact_match = 0
    diff_match = 0
    avg_rider_wait_time = 0
    count_of_user = 0
    print("SIIIIIIIIIIIIIIIIIIIIIIIIIIMMMMMMMMMMMMUUUUUUUUUUUUUUULLLLLLLLLLLLLLLAAAAAAAAAAAATTTTTTTIIIIIIIIIIOOOOOOOOONNNNNNN")
    print("Simulation ", i)
    print("SIIIIIIIIIIIIIIIIIIIIIIIIIIMMMMMMMMMMMMUUUUUUUUUUUUUUULLLLLLLLLLLLLLLAAAAAAAAAAAATTTTTTTIIIIIIIIIIOOOOOOOOONNNNNNN")
    #for i in range(0, len(Uttlist)):
     #   for j in range(0, len(riderList)):
            #print("---------For UTT:", Uttlist[i], ", for riders:", riderList[j], "--------------------")
    time_start = datetime.now().strftime(constants.TIME_STRING)
    actual_time_start = datetime.now()

    while ridersMatchingCount < riderCheck_int:
                ridersMatching, ridersMatched, requiredDrivers, exact_close_match, different_char_match, tripId, avg_waiting_time, usercount = matching_Phase5a.mainResults(
                    UTT, riderCheck_int)
                print("For traversed riders", ridersMatching, "ridersMatched", ridersMatched, "requiredDrivers", requiredDrivers)
                print("Close Match", exact_close_match, "Diff Charac Match", different_char_match)
                ridersMatchingCount += ridersMatching
                ridersMatchedCount += ridersMatched
                requiredDriversCount += requiredDrivers
                totalRidersInPool += ridersMatched
                avg_rider_wait_time += avg_waiting_time
                count_of_user += usercount
                #totalRidersInPool = totalRidersInPool + ridersMatched
                exact_match += exact_close_match
                diff_match += different_char_match
                trip_ids.append(tripId)
                print(
                    "---------------------------------****UTTWhile***-----------------------------------------------------------------------------")
                print("Riders Traversed :", ridersMatchingCount, "Riders Restricted Limit: ", riderCheck, "Match Count:", ridersMatchedCount)
                print("Drivers Required:", requiredDriversCount, "With UTT:", UTT, "Total Riders In Pool:",
                      totalRidersInPool)
                print("Exact Match: ", exact_match, "Diff Match: ", diff_match)
                print("Total Rider Waiting Time in This Trip:", round(avg_rider_wait_time, 2), "Usercount: ", count_of_user)
                avg = avg_rider_wait_time/count_of_user
                avg = round(avg, 2)
                print("Avg Waiting Time: ", avg)
                print(
                    "---------------------------------****UTTWhile***-----------------------------------------------------------------------------")

    time_end = datetime.now().strftime(constants.TIME_STRING)
    actual_time_end = datetime.now()
    diff_secs, diff_mins = commons.time_diff(actual_time_start, actual_time_end)
    average_rider_waiting_time_of_simulation = (avg_rider_wait_time / count_of_user)
    average_rider_waiting_time_of_simulation = round(average_rider_waiting_time_of_simulation, 2)
    print("---------------------------------****UTTProgramOutput***-----------------------------------------------------------------------------")
    print("For Total:", ridersMatchingCount, "For Riders: ", riderCheck, "Match Count:", ridersMatchedCount)
    print("Drivers Required:", requiredDriversCount, "With UTT:", UTT, "Total Riders In Pool:",
          totalRidersInPool)
    print("Exact Match: ", exact_match, "Diff Match: ", diff_match)
    print("---------------------------------****UTTProgramOutput***-----------------------------------------------------------------------------")
    matching_rate = totalRidersInPool/riderCheck_int
    document = {
                constants.TOTAL_RIDERS_CHECKED: ridersMatchingCount,
                constants.TOTAL_RIDERS_MATCHED: ridersMatchedCount,
                constants.TOTAL_RIDERS_IN_POOL: totalRidersInPool,
                "exact_match_count": exact_match,
                "diff_match_count": diff_match,
                constants.FOR_RIDER_COUNT: riderCheck_int,
                "matching_rate": matching_rate,
                "average_rider_waiting_time": average_rider_waiting_time_of_simulation,
                constants.TOTAL_DRIVERS: requiredDriversCount,
                constants.UTT: UTT,
                "tripQs": trip_ids,
                constants.TRIP_START_TIME: time_start,
                constants.TRIP_END_TIME: time_end,
                constants.TRIP_DIFF_SECS: diff_secs,
                constants.TRIP_DIFF_MINS: diff_mins
            }
    print(document)

    results_phase1 = db.resultsCollection
    doc_id = results_phase1.insert_one(document)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@    Inserted A Document in Results @@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


