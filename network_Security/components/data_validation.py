import sys,os
from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging
from network_Security.entity.config_entity import DataValidationConfig
from network_Security.entity.artifact_entity import DataIngestionArtifact
from scipy.stats import ks_2samp
from network_Security.entity.artifact_entity import DataValdationArtifact
import pandas as pd
from network_Security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_Security.utils.main_utils.utils import read_yaml_file,wirte_yaml_file

class Data_Validation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
    @staticmethod    
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"required columns: {number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}") 

            if len(dataframe.columns)==number_of_columns:
                return True
            
            return False   
        except Exception as e:
            raise CustomException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_stauts":is_found
                }})        

            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            wirte_yaml_file(file_path=drift_report_file_path,content=report)    
            return status
        except  Exception  as e:
            raise CustomException(e,sys)

        
    def initiate_data_validation(self)->DataValdationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            test_dataf=self.read_data(test_file_path)
            trained_dataf=self.read_data(train_file_path)

            """validate the data """
            status=self.validate_number_of_columns(dataframe=trained_dataf)

            if not status:
                error_message=f"train Dataframe does not contain all columns. \n"
            status=self.validate_number_of_columns(test_dataf)
            if not status:
                error_message=f"test datframe are not complete.\n"
            ## late check datadrift
            status=self.detect_dataset_drift(base_df=trained_dataf,current_df=test_dataf)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok= True)


            trained_dataf.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )


            test_dataf.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )   

            data_validation_artifact = DataValdationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path,
                )    
            return data_validation_artifact



 
        except  Exception as e:
            raise CustomException(e,sys)    











            
           



