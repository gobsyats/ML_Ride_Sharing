from dbconnection import db
import constants

zoneHits = db.zonehits

def zoneHitsUTT(UTT):
    keys = range(1, constants.TOTAL_ZONES)
    values = 0
    zoneHitsTrack = {constants.UTT: UTT}
    for i in keys:
            zoneHitsTrack[i] = values
    print(zoneHitsTrack)
    zoneHitIds = zoneHits.insert_one(zoneHitsTrack)

for i in range(1,7):
    UTT = 5*i
    zoneHitsUTT(UTT)

cursor = zoneHits.find({})
count = cursor.count(True)

print('Found ', count, 'records in ZoneHits')