import os
import sys
import pandas as pd
from scipy.stats import ks_2samp
from network_Security.exceptions.exception import CustomException
from network_Security.log.logger import logging
from network_Security.entity.config_entity import DataValidationConfig
from network_Security.entity.artifact_entity import DataIngestionArtifact, DataValdationArtifact
from network_Security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_Security.utils.main_utils.utils import read_yaml_file, wirte_yaml_file

class Data_Validation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        self.expected_columns = [next(iter(column)) if isinstance(column, dict) else column for column in self._schema_config.get("columns", [])]

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as error:
            raise CustomException(error, sys) from error

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        return list(dataframe.columns) == self.expected_columns

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        report = {}
        status = True
        for column in base_df.columns:
            left, right = base_df[column].dropna(), current_df[column].dropna()
            if pd.api.types.is_numeric_dtype(left) and len(left) and len(right):
                p_value = float(ks_2samp(left, right).pvalue)
            else:
                p_value = 1.0
            drift = p_value < threshold
            status = status and not drift
            report[column] = {"p_value": p_value, "drift_status": drift}
        wirte_yaml_file(self.data_validation_config.drift_report_file_path, report, replace=True)
        return status

    def initiate_data_validation(self) -> DataValdationArtifact:
        try:
            train = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test = self.read_data(self.data_ingestion_artifact.test_file_path)
            for name, frame in (("train", train), ("test", test)):
                if not self.validate_number_of_columns(frame):
                    raise ValueError(f"{name} dataset columns do not match data_schema/schema.yaml")
                if frame.empty:
                    raise ValueError(f"{name} dataset is empty")
            if train.isna().all().any() or test.isna().all().any():
                raise ValueError("Dataset contains a column with no usable values")
            self.detect_dataset_drift(train, test)
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            train.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test.to_csv(self.data_validation_config.valid_test_file_path, index=False)
            return DataValdationArtifact(True, self.data_validation_config.valid_train_file_path, self.data_validation_config.valid_test_file_path, None, None, self.data_validation_config.drift_report_file_path)
        except Exception as error:
            raise CustomException(error, sys) from error
