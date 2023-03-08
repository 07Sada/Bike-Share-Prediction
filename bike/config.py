from dataclasses import dataclass
import pymongo
from datetime import datetime
import os, sys 
from dotenv import load_dotenv

load_dotenv()

@dataclass
class EnvironmentVariable():
    mongo_db_url = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariable()

mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
