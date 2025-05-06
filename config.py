import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'new_password')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'coach')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key') 