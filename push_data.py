import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()
Mongo_db_url=os.getenv("MONGO_URI")
print(Mongo_db_url)

import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo
from network_Security.logging import logger
from network_Security.exceptions import exception


class network_DataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise exception(e,sys)
        

    def cv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise exception(e,sys)     
        

    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records


            self.monogo_client=pymongo.MongoClient(Mongo_db_url)
            self.database=self.monogo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise exception(e,sys)


if __name__=="__main__":
    file_path="Network_data\phisingData.csv"
    database="first"
    collection="NetworkData"
    networkobj=network_DataExtraction()
    records=networkobj.cv_to_json_convertor(file_path=file_path)
    no_of_records=networkobj.insert_data_to_mongodb(records=records,database=database,collection=collection)
    print(no_of_records)

        