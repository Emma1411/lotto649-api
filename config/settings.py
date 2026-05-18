import os
from dotenv import load_dotenv

load_dotenv()

ENV          = os.getenv("ENV", "development")
APP_NAME     = os.getenv("APP_NAME", "lotto649-api")
API_VERSION  = os.getenv("API_VERSION", "v1")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
MODEL_PATH   = os.getenv("MODEL_PATH", "../lotto649-data/models/model.pkl")
POOL_PATH    = os.getenv("POOL_PATH",  "../lotto649-data/models/top20.csv")