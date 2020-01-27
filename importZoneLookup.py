from dbconnection import db
import pandas as pd

zone_lookup = db.zone_lookup
data = "taxi_zone_lookup.csv"
df = pd.read_csv(data)
records_ = df.to_dict(orient='records')
result = db.zone_lookup.insert_many(records_ )
