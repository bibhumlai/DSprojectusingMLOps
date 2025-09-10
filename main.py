from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import STAGE_NAME, DataIngestionTRainingPipeline

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