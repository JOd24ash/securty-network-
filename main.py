from network_Security.components.data_ingestion import DataIngestion

from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging
import sys
from network_Security.entity.config_entity import DataIngestionConfig
from network_Security.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        tainingpipelineConfig=TrainingPipelineConfig()
        dataIngestionConfig=DataIngestionConfig(tainingpipelineConfig)
        dataIngestion=DataIngestion(dataIngestionConfig)
        dataingestionartifact=dataIngestion.initiate_data_ingestion()
        print(dataingestionartifact)

    except Exception as e:
        raise CustomException(e,sys)    

