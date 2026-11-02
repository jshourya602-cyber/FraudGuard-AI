
import os
from pathlib import Path
from dotenv import load_dotenv

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


class Config:

    # Flask settings
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-change-before-deployment"
    )

    # MySQL settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "fraud_detection")

    # Project directories
    BASE_DIR = BASE_DIR
    MODEL_DIR = BASE_DIR / "model"
    DATASET_DIR = BASE_DIR / "dataset"

    # Machine learning settings
    RANDOM_STATE = 42
    TEST_SIZE = 0.20


# Create model and dataset directories if missing
Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
Config.DATASET_DIR.mkdir(parents=True, exist_ok=True)
