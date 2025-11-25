import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        
    def get_connection(self):
        """Conexión con psycopg2"""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
    
    def get_engine(self):
        """Engine de SQLAlchemy para pandas"""
        connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(connection_string)