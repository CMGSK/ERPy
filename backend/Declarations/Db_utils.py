import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import Connection


def generate_session():
    load_dotenv()

    if bool(int(os.environ.get('IS_LOCAL_DATABASE'))):
        engine = create_engine('sqlite:///Database/erp.db', echo=True)
    else:
        engine = Connection.engine

    session = sessionmaker(bind=engine)
    return session()


def generate_engine():
    load_dotenv()

    if bool(int(os.environ.get('IS_LOCAL_DATABASE'))):
        return create_engine('sqlite:///Database/erp.db', echo=True)
    else:
        return Connection.engine
