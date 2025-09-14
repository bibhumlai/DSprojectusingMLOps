from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import STAGE_NAME, DataIngestionTRainingPipeline
from src.datascience.pipeline.data_validation_pipeline import STAGE_NAME, DataValidationTrainingPipeline
from src.datascience.pipeline.data_transformation_pipeline import STAGE_NAME, DataTransformationTrainingPipeline
logger.info("Welcome to custom logger DS")


STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
    obj = DataIngestionTRainingPipeline()
    obj.initiate_Data_ingestion()
    logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Validation  Stage"
try:
    logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.initiate_Data_Validation()
    logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="Data Transformation Stage"
try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_Data_Transformation()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
except Exception as e:
        logger.exception(e)
        raise e
