import os
import yaml
from src.datascience import  logger
import joblib
import json
from ensure import ensure_annotations ## used to get correct error liek if int is string
from box import ConfigBox ## is to be bring simplification to the key value pair
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """ reads yaml filr and returns
    args: 
    path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file
    
    returns:
        ConfigBox: CofigBox type

    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded sucessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """ Create list of directories
    arges:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to one """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:logger.info(f"created directory at path :{path}")


@ensure_annotations
def save_json(path:Path, data:dict):
    """ Save json data
    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
        """
    with open(path, "w") as f:
        json.dump(data,f,indent=4)

    logger.info(f"json file saved at : {path}")



@ensure_annotations
def load_json(path:Path, data:dict):
    """ load json data
    Args:
        path (Path): path to json file
        
    Returns:
        ConfigBox: data as class attributes instead of dict
        """
    with open(path, "w") as f:
        content=json.load(f)

    logger.info(f"json file sucessfully from : {path}")
    return ConfigBox(content)



@ensure_annotations
def save_bin(path:Path, data:any):
    """ Save json data
    Args:
        path (Path): path to binary file
        data (any): data to be saved in binary
        """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file is saved at : {path}")



@ensure_annotations
def load_bin(path:Path):
    """ Save json data
    Args:
        path (Path): path to binary file
    
    returns:
        Any: object stored in the file
        """
    data =joblib.load(path)
    logger.info(f"binary file is loaded from : {path}")
    return data