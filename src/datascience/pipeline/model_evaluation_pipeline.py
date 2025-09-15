
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.model_evaluation import ModelEvaluation
from src.datascience import logger
from pathlib import Path

STAGE_NAME="Model Evaluation  Stage"
class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def initiate_model_Evaluation(self):
        try:
            config = ConfigurationManager()
            model_eval_config = config.get_model_evaluation_config()
            logger.info(f"Model Evaluation Config: {model_eval_config}")
            model_eval = ModelEvaluation(config=model_eval_config)
            model_eval.log_into_mlflow()
        except Exception as e:
            logger.exception(e)
            raise e    
            
if  __name__ == '__main__':

    try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started  <<<<<<<<<<<<<")
        obj = ModelEvaluationPipeline()
        obj.initiate_model_Evaluation()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed  <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e