import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(f"mysql+pymysql://"
                       f"{os.environ.get('DB_USER')}:"
                       f"{os.environ.get('DB_PASSWORD')}@"
                       f"{os.environ.get('IP_ACCESS')}:"
                       f"{os.environ.get('DB_PORT')}/"
                       f"{os.environ.get('DB_SCHEMA')}?charset=utf8mb4")