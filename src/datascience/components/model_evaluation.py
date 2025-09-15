from src.datascience.constants import *
from src.datascience.utils.common import read_yaml,create_directories,save_json
from src.datascience.entity.config_entity import (ModelEvaluationConfig)
import pandas as pd
import os
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
from src.datascience import logger
import mlflow.sklearn
import joblib

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def eval_metrics(self, actual, predicted) -> dict:
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        r2_square = r2_score(actual, predicted)
        return  rmse, mae, r2_square
    
    def log_into_mlflow(self):
        
        test_data = pd.read_csv(self.config.test_data_path)
        logger.info(f"Test data shape: {test_data.shape}")
        model = joblib.load(self.config.model_path)
        logger.info(f"Model: {model}")
        test_x= test_data.drop(columns=[self.config.target_column], axis=1)
        test_y= test_data[self.config.target_column]
        
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
    
        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)
            (rmse, mae, r2_square) = self.eval_metrics(test_y, predicted_qualities)
            logger.info(f"Elasticnet model (alpha={self.config.all_params['alpha']}, l1_ratio={self.config.all_params['l1_ratio']})")
            logger.info(f"  RMSE: {rmse}")
            logger.info(f"  MAE: {mae}")
            logger.info(f"  R2: {r2_square}")
            
            ##SAVE METRICS
            scores = ({"rmse": rmse, "mae": mae, "r2_square": r2_square})
            save_json(path=Path(self.config.metric_file_name), data= scores)
            mlflow.log_params(self.config.all_params)
            mlflow.log_param("alpha", self.config.all_params['alpha'])
            mlflow.log_param("l1_ratio", self.config.all_params['l1_ratio'])
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2_square", r2_square)
            
            model_path = Path(self.config.root_dir) / "model"
            mlflow.sklearn.save_model(model, path=str(model_path))
            mlflow.log_artifacts(str(model_path), artifact_path="model")