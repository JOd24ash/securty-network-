from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging

from network_Security.entity.config_entity import DataIngestionConfig

from network_Security.entity.artifact_entity import DataIngestionArtifact
import os
import pandas as pd
import sys
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split  # type: ignore[import]
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_url=os.getenv("MONGO_URL")
import certifi
ca = certifi.where()



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise CustomException(e,sys)
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_url, tlsCAFile=ca)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"])
            df.replace({"na":np.nan},inplace=True)    
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_spilt,random_state=42)
            logging.info("performed train test split on the datframe")

            logging.info("exited split_data_ as train test method of dat ingestion class")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("the date is exported to  train and test data")
        except Exception as e:
            raise CustomException(e,sys)

        
    def initiate_data_ingestion(self):
        try:
            dataFrame=self.export_collection_as_dataframe()
            dataFrame=self.export_data_to_feature_store(dataframe=dataFrame)
            self.split_data_as_train_test(dataframe=dataFrame)

            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)    