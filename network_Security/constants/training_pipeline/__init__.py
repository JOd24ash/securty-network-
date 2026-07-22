import os
import sys
import numpy as np
import pandas as pd

"""
defining common constant variable for training pipline
"""
TARGET_COLUMN="Result"
PIPELINE_NAME: str="NetworkSecurity"
ARITFACT_DIR: str="Artifacts"
FILE_NAME : str ="NetworkData.csv"

TRAIN_FILE_NAME: str="train.csv"
TEST_FILE_NAME:str="test.csv"

"""
Data ingestion related constant start with Data_ingetion Var name
"""
DATA_INGESTION_COLLECTION_NAME: str="NetworkData"
DATA_INGESTION_DATABASE_NAME :str="first"
DATA_INGESTION_DIR_NAME: str="data_ingestion.py"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")
"""
Data Validation related constant start with Data validation VAriable name
"""
DATA_VALIDATION__DIR_NAME:str ="data_validation"
DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_INVALID_DIR: str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"


"""
Data Transformation related constant start with Data_transformation Var name
"""

DATA_TRANSFORMATION_DIR_NAME: str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR :str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"


"""

"""