import sys
from network_Security.components.data_ingestion import DataIngestion
from network_Security.components.data_validation import Data_Validation
from network_Security.components.data_transformation import DataTransformation
from network_Security.components.model_trainer import ModelTrainer
from network_Security.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig)
from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging

def run_training_pipeline():
    pipeline_config = TrainingPipelineConfig()
    ingestion = DataIngestion(DataIngestionConfig(pipeline_config))
    ingestion_artifact = ingestion.initiate_data_ingestion()
    validation = Data_Validation(ingestion_artifact, DataValidationConfig(pipeline_config))
    validation_artifact = validation.initiate_data_validation()
    transformation = DataTransformation(DataTransformationConfig(pipeline_config))
    transformation_artifact = transformation.initiate_data_transformation(validation_artifact)
    trainer = ModelTrainer(ModelTrainerConfig(pipeline_config))
    model_artifact = trainer.initiate_model_trainer(transformation_artifact, validation_artifact)
    logging.info("Training pipeline completed: %s", model_artifact)
    return model_artifact

if __name__ == "__main__":
    try:
        print(run_training_pipeline())
    except Exception as error:
        raise CustomException(error, sys) from error
