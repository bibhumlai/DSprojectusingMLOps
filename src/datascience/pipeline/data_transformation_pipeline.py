
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_transformation import DataTransformation
from src.datascience import logger
from pathlib import Path
STAGE_NAME="Data Transformation Stage"
class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_Data_Transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), 'r') as f:
                status = f.read().split(" ")[-1]
            if status == "True":
                config= ConfigurationManager()
                data_Transformation_config=config.get_data_transformation_config()
                data_Transformation= DataTransformation(config=data_Transformation_config)
                data_Transformation.train_test_data_splitting()
            else:
                raise Exception("Data Validation Failed, Please check the logs")
        except Exception as e:
            raise e
            print(e)



if  __name__ == '__main__':

    try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_Data_Transformation()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e