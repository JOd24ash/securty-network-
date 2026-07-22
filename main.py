from network_Security.components.data_ingestion import DataIngestion
from network_Security.components.data_validation import Data_Validation
from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging
import sys
from network_Security.entity.config_entity import DataIngestionConfig,DataValidationConfig
from network_Security.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        tainingpipelineConfig=TrainingPipelineConfig()
        dataIngestionConfig=DataIngestionConfig(tainingpipelineConfig)
        dataIngestion=DataIngestion(dataIngestionConfig)
        dataingestionartifact=dataIngestion.initiate_data_ingestion()
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(tainingpipelineConfig)
        data_validation=Data_Validation(dataingestionartifact,data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation complted")
        print(data_validation_artifact)

    except Exception as e:
        raise CustomException(e,sys)    

