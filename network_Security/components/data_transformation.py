import os
import sys
import dill
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from network_Security.constants.training_pipeline import TARGET_COLUMN
from network_Security.entity.artifact_entity import DataTransformationArtifact
from network_Security.exceptions.exception import CustomException

class DataTransformation:
    def __init__(self, config):
        self.config = config

    def initiate_data_transformation(self, validation_artifact):
        try:
            train = pd.read_csv(validation_artifact.valid_train_file_path)
            test = pd.read_csv(validation_artifact.valid_test_file_path)
            if TARGET_COLUMN not in train or TARGET_COLUMN not in test:
                raise ValueError(f"Required target column {TARGET_COLUMN!r} is missing")
            features = [column for column in train.columns if column != TARGET_COLUMN]
            if not features:
                raise ValueError("Dataset has no feature columns")
            numeric = train[features].select_dtypes(include="number").columns.tolist()
            categorical = [column for column in features if column not in numeric]
            transformers = []
            if numeric:
                transformers.append(("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric))
            if categorical:
                transformers.append(("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent"))]), categorical))
            preprocessor = ColumnTransformer(transformers)
            x_train = preprocessor.fit_transform(train[features])
            x_test = preprocessor.transform(test[features])
            os.makedirs(os.path.dirname(self.config.transformed_train_file_path), exist_ok=True)
            pd.DataFrame(x_train).to_csv(self.config.transformed_train_file_path, index=False)
            pd.DataFrame(x_test).to_csv(self.config.transformed_test_file_path, index=False)
            os.makedirs(os.path.dirname(self.config.preprocessor_object_file_path), exist_ok=True)
            with open(self.config.preprocessor_object_file_path, "wb") as stream:
                dill.dump(preprocessor, stream)
            return DataTransformationArtifact(self.config.transformed_train_file_path, self.config.transformed_test_file_path, self.config.preprocessor_object_file_path, features)
        except Exception as error:
            raise CustomException(error, sys) from error
