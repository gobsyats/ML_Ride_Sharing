from dbconnection import db
import pandas as pd
from datetime import datetime


resultCollectionFile = db.resultsCollection
cursor = resultCollectionFile.find()
dateStr = datetime.now()
resultStr = str(dateStr)
resultStr = resultStr.replace(" ", "")
df = pd.DataFrame(list(cursor))
df.to_csv('results_collection_ml_v11.csv', index=False)