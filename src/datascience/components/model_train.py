import pandas as pd
import os
from src.datascience.utils.common import save_json,load_json
from sklearn.linear_model import ElasticNet
import joblib
from src.datascience import logger
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.entity.config_entity import ModelTrainerConfig

class model_trainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        logger.info("Loading training and test data")
        train_data = pd.read_csv(self.config.train_date_path)
        test_data = pd.read_csv(self.config.test_data_path)

        logger.info("Splitting features and target")
        X_train = train_data.drop(columns=[self.config.target_column], axis=1)
        y_train = train_data[self.config.target_column]

        X_test = test_data.drop(columns=[self.config.target_column], axis=1)
        y_test = test_data[self.config.target_column]

        logger.info("Training the model")
        lr = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio, random_state=42)
        lr.fit(X_train, y_train)

        logger.info("Saving the model")
        os.makedirs(self.config.root_dir, exist_ok=True)
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(lr, model_path)
        logger.info(f"Model saved at {model_path}")
        
        logger.info("Model training completed successfully")

if __name__ == "__main__":
    try:
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_instance = model_trainer(config=model_trainer_config)
        model_trainer_instance.train_model()
        logger.info("Model training completed successfully.")
    except Exception as e:
        logger.exception(e)
        raise e