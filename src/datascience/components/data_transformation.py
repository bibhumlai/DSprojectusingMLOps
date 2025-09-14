from src.datascience import logger
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from pathlib import Path
from src.datascience.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config=config
        
    def train_test_data_splitting(self):
        data=pd.read_csv(self.config.data_path)
        train, test = train_test_split(data, test_size=0.2, random_state=42)
       

        train_path = os.path.join(self.config.root_dir, "train.csv")
        train.to_csv(train_path, index=False)

        test_path = os.path.join(self.config.root_dir, "test.csv")
        test.to_csv(test_path, index=False)

        logger.info(f"Train and Test data saved in {self.config.root_dir}")
        logger.info(train.shape)
        logger.info(test.shape)
        print(train.shape
                )
        print(test.shape)
        