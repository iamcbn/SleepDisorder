import os
from pathlib import Path

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent

# Directories
DATA_DIR = ROOT_DIR / 'data'
MODELS_DIR = ROOT_DIR / 'models'
TRANSFORMERS_DIR = ROOT_DIR / 'transformers'
APP_DIR = ROOT_DIR / 'helper'

# Files
# data directory files
DATA_FILE = DATA_DIR / 'data.csv'
PROFILE = DATA_DIR / 'Profile.png'
BANNER_IMAGE = DATA_DIR / 'banner_image.png'
NOTEBOOK_FILE = DATA_DIR / 'notebook.ipynb'
LOGO_IMAGE = DATA_DIR / 'logo.png'

# models directory files
MODEL_FILE = MODELS_DIR / 'model.pkl'
FEATURE_ENCODER = MODELS_DIR / 'feature_encoder.pkl'
TARGET_ENCODER = MODELS_DIR / 'target_encoder.pkl'
SCALER_FILE = MODELS_DIR / 'scaler.pkl'
MODEL_EVAL = MODELS_DIR / 'model_evaluation.pkl'

# transformers directories files
BMI_FILE = TRANSFORMERS_DIR / 'bmi_categorizer.py'
BP_FILE = TRANSFORMERS_DIR / 'bp_classifier.py'
FEATURE_CORRECTER = TRANSFORMERS_DIR / 'feature_correcter.py'
PIPELINE_FILE = TRANSFORMERS_DIR / 'pipeline.py'
SAVED_ENCODER = TRANSFORMERS_DIR / 'saved_encoder.py'
SAVED_SCALER = TRANSFORMERS_DIR / 'saved_scaler.py'

# utils path in app/
UTILS_FILE = APP_DIR / 'utils.py'
CONTACT_FORM = APP_DIR / 'contact_form.py'

# Important features
NUM_FEATURES = ["Age", "Sleep Duration", "Quality of Sleep",
                "Physical Activity Level", "Stress Level", "Heart Rate", "Daily Steps"]
CAT_FEATURES = ["Gender", "Occupation", "BMI Category", "BP Category"]


# Utility function to ensure paths exist
def ensure_dirs():
    for path in [DATA_DIR, MODELS_DIR, TRANSFORMERS_DIR, APP_DIR]:
        os.makedirs(path, exist_ok=True)
