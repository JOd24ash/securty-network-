import os
import sys
import dill
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from network_Security.constants.training_pipeline import TARGET_COLUMN
from network_Security.entity.artifact_entity import ModelTrainerArtifact
from network_Security.exceptions.exception import CustomException

class ModelTrainer:
    def __init__(self, config):
        self.config = config

    def initiate_model_trainer(self, transformation_artifact, validation_artifact):
        try:
            train = pd.read_csv(validation_artifact.valid_train_file_path)
            test = pd.read_csv(validation_artifact.valid_test_file_path)
            with open(transformation_artifact.preprocessor_object_file_path, "rb") as stream:
                preprocessor = dill.load(stream)
            x_train = preprocessor.transform(train[transformation_artifact.feature_names])
            x_test = preprocessor.transform(test[transformation_artifact.feature_names])
            y_train, y_test = train[TARGET_COLUMN], test[TARGET_COLUMN]
            if y_train.nunique() < 2:
                raise ValueError("Training data must contain at least two target classes")
            model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=-1)
            model.fit(x_train, y_train)
            predictions = model.predict(x_test)
            accuracy = float(accuracy_score(y_test, predictions))
            f1 = float(f1_score(y_test, predictions, average="weighted", zero_division=0))
            os.makedirs(os.path.dirname(self.config.trained_model_file_path), exist_ok=True)
            with open(self.config.trained_model_file_path, "wb") as stream:
                dill.dump({"model": model, "preprocessor": preprocessor, "feature_names": transformation_artifact.feature_names}, stream)
            return ModelTrainerArtifact(self.config.trained_model_file_path, accuracy, f1)
        except Exception as error:
            raise CustomException(error, sys) from error
