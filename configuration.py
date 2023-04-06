from database.models import Base
from database.models import User, Article
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_DOMAIN = os.getenv('DB_DOMAIN')