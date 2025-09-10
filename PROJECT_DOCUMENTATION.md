# MLOps Data Science Project - Complete Implementation Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Step-by-Step Implementation Guide](#step-by-step-implementation-guide)
4. [Configuration Files](#configuration-files)
5. [Components Implementation](#components-implementation)
6. [Pipeline Implementation](#pipeline-implementation)
7. [Setup and Installation](#setup-and-installation)
8. [Usage Instructions](#usage-instructions)
9. [Project Architecture](#project-architecture)

## Project Overview

This is a comprehensive MLOps (Machine Learning Operations) project built using Python that demonstrates best practices for data science project structure, configuration management, logging, and pipeline orchestration. The project focuses on wine quality prediction using a structured, modular approach.

### Key Features:
- **Modular Architecture**: Clean separation of concerns with components, pipelines, and configuration
- **Configuration Management**: YAML-based configuration for easy parameter tuning
- **Logging System**: Comprehensive logging for debugging and monitoring
- **Data Pipeline**: Automated data ingestion and validation pipelines
- **Schema Validation**: Data quality assurance through schema validation
- **Docker Support**: Containerization for deployment
- **Research Notebooks**: Jupyter notebooks for exploratory data analysis

## Project Structure

```
DSusingMLOps/
├── artifacts/                          # Generated artifacts and data
│   ├── data_ingestion/
│   │   ├── data/                       # Extracted data files
│   │   └── data.zip                    # Downloaded data archive
│   └── data_validation/
│       └── status.txt                  # Validation status file
├── config/
│   └── config.yaml                     # Main configuration file
├── logs/
│   └── logging.log                     # Application logs
├── research/                           # Jupyter notebooks for EDA
│   ├── 1_data_ingestion.ipynb
│   ├── 2_data_validation.ipynb
│   └── research.ipynb
├── src/
│   └── datascience/                    # Main source code
│       ├── __init__.py                 # Logger setup
│       ├── components/                 # Core components
│       │   ├── data_ingestion.py
│       │   └── data_validation.py
│       ├── config/                     # Configuration management
│       │   └── configuration.py
│       ├── constants/                  # Project constants
│       │   └── __init__.py
│       ├── entity/                     # Data classes
│       │   └── config_entity.py
│       ├── pipeline/                   # Pipeline orchestration
│       │   ├── data_ingestion_pipeline.py
│       │   └── data_validation_pipeline.py
│       └── utils/                      # Utility functions
│           └── common.py
├── templates/                          # Web templates
│   └── index.html
├── main.py                             # Main entry point
├── template.py                         # Project structure generator
├── requirements.txt                    # Python dependencies
├── params.yaml                         # Model parameters
├── schema.yaml                         # Data schema definition
├── setup.py                            # Package setup
├── Dockerfile                          # Docker configuration
└── README.md                           # Project documentation
```

## Step-by-Step Implementation Guide

### Step 1: Project Initialization and Structure Setup

#### 1.1 Create Project Structure
```python
# template.py - Project structure generator
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

project_name = "datascience"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "research/research.ipynb",
    "templates/index.html"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory {filedir} for file : {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")
```

**Run this script to create the initial project structure:**
```bash
python template.py
```

### Step 2: Logger Setup

#### 2.1 Configure Logging System
```python
# src/datascience/__init__.py
import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s : %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "logging.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("DatascienceLogging")

__all__ = ["logger"]
```

### Step 3: Constants and Configuration

#### 3.1 Define Project Constants
```python
# src/datascience/constants/__init__.py
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")
```

#### 3.2 Create Configuration Files

**config/config.yaml:**
```yaml
artifacts_root: artifacts

data_ingestion:
  root_dir: artifacts/data_ingestion
  source_url: "https://github.com/krishnaik06/datasets/raw/main/winequality-data.zip"
  local_data_file: artifacts/data_ingestion/data.zip
  unzip_dir: artifacts/data_ingestion/data/

data_validation:
  root_dir: artifacts/data_validation
  unzip_data_dir: artifacts/data_ingestion/data/winequality-red.csv
  STATUS_FILE: artifacts/data_validation/status.txt
```

**schema.yaml:**
```yaml
COLUMNS:
  fixed acidity: float64
  volatile acidity: float64
  citric acid: float64
  residual sugar: float64
  chlorides: float64
  free sulfur dioxide: float64
  total sulfur dioxide: float64
  density: float64
  pH: float64
  sulphates: float64
  alcohol: float64
  quality: int64

TARGET_COLUMN:
  name: quality
```

**params.yaml:**
```yaml
Key: Value
```

### Step 4: Utility Functions

#### 4.1 Implement Common Utilities
```python
# src/datascience/utils/common.py
import os
import yaml
from src.datascience import logger
import joblib
import json
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns ConfigBox type"""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create list of directories"""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at path: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Save json data"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path):
    """load json data"""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file successfully loaded from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(path: Path, data: any):
    """Save binary data"""
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file is saved at: {path}")

@ensure_annotations
def load_bin(path: Path):
    """Load binary data"""
    data = joblib.load(path)
    logger.info(f"binary file is loaded from: {path}")
    return data
```

### Step 5: Entity Classes

#### 5.1 Define Configuration Entities
```python
# src/datascience/entity/config_entity.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

@dataclass
class DataValidationConfig():
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict
```

### Step 6: Configuration Manager

#### 6.1 Implement Configuration Management
```python
# src/datascience/config/configuration.py
from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories
from src.datascience.entity.config_entity import (DataIngestionConfig, DataValidationConfig)

class ConfigurationManager():
    def __init__(self, config_filepath=CONFIG_FILE_PATH, 
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            unzip_data_dir=config.unzip_data_dir,
            all_schema=schema
        )
        return data_validation_config
```

### Step 7: Component Implementation

#### 7.1 Data Ingestion Component
```python
# src/datascience/components/data_ingestion.py
from urllib import request
from src.datascience import logger
import zipfile
from src.datascience.entity.config_entity import DataIngestionConfig
import os

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists")

    def extract_zip_file(self):
        """extracts the zip file into the data directory"""
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)
```

#### 7.2 Data Validation Component
```python
# src/datascience/components/data_validation.py
from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories
from src.datascience.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
    
    def validate_all_columns(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status
        except Exception as e:
            raise e
```

### Step 8: Pipeline Implementation

#### 8.1 Data Ingestion Pipeline
```python
# src/datascience/pipeline/data_ingestion_pipeline.py
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_ingestion import DataIngestion
from src.datascience import logger

STAGE_NAME = "data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
```

#### 8.2 Data Validation Pipeline
```python
# src/datascience/pipeline/data_validation_pipeline.py
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_validation import DataValidation
from src.datascience import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
```

### Step 9: Main Entry Point

#### 9.1 Create Main Application
```python
# main.py
from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import STAGE_NAME, DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import STAGE_NAME, DataValidationTrainingPipeline

logger.info("Welcome to custom logger DS")

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.initiate_data_ingestion()
    logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>>>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.initiate_data_validation()
    logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e
```

### Step 10: Dependencies and Setup

#### 10.1 Create Requirements File
```txt
# requirements.txt
pandas
mlflow
notebook
numpy
scikit-learn
matplotlib
python-box
pyYAML
tqdm
ensure
joblib
types-pyYAML
FLASK
FLASK-Cors
```

#### 10.2 Setup Script
```python
# setup.py
# (Empty file - can be populated with package setup if needed)
```

## Configuration Files

### config/config.yaml
This file contains all the configuration parameters for the project:
- **artifacts_root**: Root directory for all generated artifacts
- **data_ingestion**: Configuration for data download and extraction
- **data_validation**: Configuration for data validation process

### schema.yaml
Defines the expected data schema:
- **COLUMNS**: Column names and their expected data types
- **TARGET_COLUMN**: The target variable for machine learning

### params.yaml
Contains model parameters (currently minimal, can be expanded)

## Components Implementation

### Data Ingestion Component
- **Purpose**: Downloads and extracts data from external sources
- **Key Methods**:
  - `download_file()`: Downloads data from URL
  - `extract_zip_file()`: Extracts downloaded zip files

### Data Validation Component
- **Purpose**: Validates data against predefined schema
- **Key Methods**:
  - `validate_all_columns()`: Checks if all columns match the schema

## Pipeline Implementation

### Data Ingestion Pipeline
- Orchestrates the data ingestion process
- Uses configuration manager to get settings
- Creates data ingestion component and executes the process

### Data Validation Pipeline
- Orchestrates the data validation process
- Validates data quality and schema compliance
- Writes validation status to a file

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or create the project directory**
2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the project structure generator**:
   ```bash
   python template.py
   ```

## Usage Instructions

### Running the Complete Pipeline
```bash
python main.py
```

### Running Individual Components
```bash
# Data Ingestion only
python src/datascience/pipeline/data_ingestion_pipeline.py

# Data Validation only
python src/datascience/pipeline/data_validation_pipeline.py
```

### Checking Logs
Logs are written to `logs/logging.log` and also displayed in the console.

### Validation Status
Check `artifacts/data_validation/status.txt` for data validation results.

## Project Architecture

### Design Patterns Used

1. **Configuration Management Pattern**: Centralized configuration using YAML files
2. **Pipeline Pattern**: Sequential processing of data through defined stages
3. **Component Pattern**: Modular, reusable components for specific tasks
4. **Entity Pattern**: Data classes for configuration and data transfer objects

### Key Benefits

1. **Modularity**: Each component has a single responsibility
2. **Configurability**: Easy to modify parameters without code changes
3. **Logging**: Comprehensive logging for debugging and monitoring
4. **Scalability**: Easy to add new components and pipelines
5. **Maintainability**: Clean code structure with clear separation of concerns

### Future Enhancements

1. **Model Training Pipeline**: Add machine learning model training
2. **Model Evaluation Pipeline**: Add model evaluation and metrics
3. **Model Deployment**: Add model serving and deployment
4. **CI/CD Integration**: Add GitHub Actions for automated testing
5. **Monitoring**: Add model and data drift monitoring
6. **API Development**: Create REST API for model inference

## Conclusion

This MLOps project demonstrates a professional approach to data science project organization. It provides a solid foundation for building scalable, maintainable machine learning pipelines with proper configuration management, logging, and modular architecture.

The step-by-step implementation guide above shows how to build each component from scratch, ensuring understanding of the underlying principles and best practices in MLOps.
