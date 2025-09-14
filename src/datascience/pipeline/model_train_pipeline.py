
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.model_train import model_trainer
from src.datascience import logger
from pathlib import Path

STAGE_NAME="Model Training Stage"
class ModelTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_trainer(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), 'r') as f:
                status = f.read().split(" ")[-1]
            if status == "True":
                config= ConfigurationManager()
                model_trainer_config=config.get_model_trainer_config()
                model_trainer_instance = model_trainer(config=model_trainer_config)
                model_trainer_instance.train_model()
            else:
                raise Exception("Data Validation Failed, Please check the logs")
        except Exception as e:
            raise e
            print(e)
            
if  __name__ == '__main__':

    try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
        obj = ModelTrainingPipeline()
        obj.initiate_model_trainer()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e