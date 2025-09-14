from calendar import c
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir : Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

@dataclass
class DataValidationConfig():
    root_dir:Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict
    
@dataclass
class DataTransformationConfig():
    root_dir:Path
    data_path: Path
    
@dataclass
class ModelTrainerConfig:
    root_dir: Path
    model_name: str
    train_date_path: Path
    test_data_path: Path
    alpha: float
    l1_ratio: float
    target_column: str
