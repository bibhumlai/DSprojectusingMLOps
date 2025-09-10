# Quick Reference Guide - MLOps Data Science Project

## 🚀 Quick Start

### 1. Setup Project
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate project structure
python template.py
```

### 2. Run Complete Pipeline
```bash
python main.py
```

### 3. Run Individual Components
```bash
# Data Ingestion only
python src/datascience/pipeline/data_ingestion_pipeline.py

# Data Validation only
python src/datascience/pipeline/data_validation_pipeline.py
```

## 📁 Project Structure Overview

```
DSusingMLOps/
├── artifacts/                 # Generated data and results
├── config/                   # Configuration files
├── logs/                     # Application logs
├── research/                 # Jupyter notebooks
├── src/datascience/          # Main source code
│   ├── components/           # Core functionality
│   ├── config/              # Configuration management
│   ├── entity/              # Data classes
│   ├── pipeline/            # Pipeline orchestration
│   └── utils/               # Utility functions
├── templates/               # Web templates
└── main.py                  # Entry point
```

## 🔧 Key Files and Their Purpose

| File | Purpose |
|------|---------|
| `main.py` | Main application entry point |
| `template.py` | Project structure generator |
| `config/config.yaml` | Main configuration file |
| `schema.yaml` | Data schema definition |
| `requirements.txt` | Python dependencies |
| `src/datascience/__init__.py` | Logger setup |
| `src/datascience/constants/__init__.py` | Project constants |
| `src/datascience/utils/common.py` | Utility functions |
| `src/datascience/entity/config_entity.py` | Configuration data classes |
| `src/datascience/config/configuration.py` | Configuration manager |
| `src/datascience/components/data_ingestion.py` | Data download/extraction |
| `src/datascience/components/data_validation.py` | Data validation |
| `src/datascience/pipeline/data_ingestion_pipeline.py` | Ingestion pipeline |
| `src/datascience/pipeline/data_validation_pipeline.py` | Validation pipeline |

## 📋 Configuration Files

### config/config.yaml
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

### schema.yaml
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

## 🔍 Monitoring and Debugging

### Check Logs
```bash
# View log file
cat logs/logging.log

# Follow logs in real-time
tail -f logs/logging.log
```

### Check Validation Status
```bash
# View validation results
cat artifacts/data_validation/status.txt
```

### Check Downloaded Data
```bash
# List downloaded files
ls -la artifacts/data_ingestion/data/
```

## 🛠️ Common Commands

### Development Commands
```bash
# Run with verbose logging
python main.py

# Test individual component
python -c "from src.datascience.components.data_ingestion import DataIngestion; print('Component loaded successfully')"

# Check configuration
python -c "from src.datascience.config.configuration import ConfigurationManager; cm = ConfigurationManager(); print(cm.config)"
```

### Debugging Commands
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Check installed packages
pip list

# Check virtual environment
which python  # Linux/Mac
where python  # Windows
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Ensure virtual environment is activated and all `__init__.py` files exist |
| Configuration errors | Check YAML syntax and file paths in config files |
| Download failures | Verify network connectivity and URL accessibility |
| Validation failures | Compare data schema with schema.yaml file |
| Permission errors | Check file/directory permissions and disk space |

### Error Messages and Solutions

**"ModuleNotFoundError"**
```bash
# Solution: Activate virtual environment and install dependencies
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**"FileNotFoundError: config/config.yaml"**
```bash
# Solution: Run template generator first
python template.py
```

**"Validation status: False"**
```bash
# Solution: Check schema.yaml matches actual data columns
# Compare with: head -1 artifacts/data_ingestion/data/winequality-red.csv
```

## 📊 Data Flow

```
1. Configuration Loading
   ↓
2. Data Ingestion
   - Download from URL
   - Extract zip file
   ↓
3. Data Validation
   - Check schema compliance
   - Write validation status
   ↓
4. Logging
   - File and console output
   - Error tracking
```

## 🔄 Adding New Components

### 1. Create Component Class
```python
# src/datascience/components/new_component.py
from src.datascience import logger
from src.datascience.entity.config_entity import NewComponentConfig

class NewComponent:
    def __init__(self, config: NewComponentConfig):
        self.config = config
    
    def execute(self):
        logger.info("Executing new component")
        # Implementation here
```

### 2. Add Configuration Entity
```python
# src/datascience/entity/config_entity.py
@dataclass
class NewComponentConfig:
    root_dir: Path
    # Add other config fields
```

### 3. Update Configuration Manager
```python
# src/datascience/config/configuration.py
def get_new_component_config(self) -> NewComponentConfig:
    config = self.config.new_component
    create_directories([config.root_dir])
    
    return NewComponentConfig(
        root_dir=config.root_dir,
        # Map other fields
    )
```

### 4. Create Pipeline
```python
# src/datascience/pipeline/new_component_pipeline.py
from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.new_component import NewComponent
from src.datascience import logger

class NewComponentPipeline:
    def __init__(self):
        pass
    
    def initiate_new_component(self):
        config = ConfigurationManager()
        new_component_config = config.get_new_component_config()
        new_component = NewComponent(config=new_component_config)
        new_component.execute()
```

## 📈 Performance Tips

1. **Use Virtual Environment**: Isolate dependencies
2. **Check Logs**: Monitor for errors and performance issues
3. **Validate Data**: Ensure data quality before processing
4. **Use Type Hints**: Improve code reliability and IDE support
5. **Handle Errors**: Implement proper error handling and logging

## 🔗 Useful Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Logging in Python](https://docs.python.org/3/library/logging.html)
- [Pathlib Documentation](https://docs.python.org/3/library/pathlib.html)

## 📝 Notes

- Always activate virtual environment before running
- Check logs for debugging information
- Validate configuration files before running
- Use type hints for better code quality
- Implement proper error handling in new components
