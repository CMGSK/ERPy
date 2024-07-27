import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

load_dotenv(Path('../.cfg/.env'))
match engine_selection := os.getenv("DB_ENGINE"):
    case "mysql":
        usr = os.getenv("DB_USER")
        pwd = os.getenv("DB_PASSWORD")
        adr = os.getenv("DB_CON_ADDR")
        por = os.getenv("DB_PORT")
        sch = os.getenv("DB_NAME")
        engine = create_engine(f'mysql+pymysql://{usr}:{pwd}@{adr}:{por}/{sch}')

    case "sqlite":
        uri = os.getenv("DB_LOCATION")
        sch = os.getenv("DB_NAME")
        engine = create_engine(f'sqlite:///{uri}/{sch}.db', echo=True)

    case "postgresql":
        usr = os.getenv("DB_USER")
        pwd = os.getenv("DB_PASSWORD")
        adr = os.getenv("DB_CON_ADDR")
        por = os.getenv("DB_PORT")
        sch = os.getenv("DB_NAME")
        engine = create_engine(f'postgresql://{usr}:{pwd}@{adr}:{por}/{sch}')

    case "sqlserver":
        # We may deprecate the ability to connect to MSSQLS because they're a bunch of fucks and
        # drivers are un-fucking-reliable and complicated as hell and will cause more problems than anything else
        usr = os.getenv("DB_USER")
        pwd = os.getenv("DB_PASSWORD")
        adr = os.getenv("DB_CON_ADDR")
        por = os.getenv("DB_PORT")
        sch = os.getenv("DB_NAME")
        ver = os.getenv("DB_MSSQL_VER")
        engine = create_engine(f'mssql+pyodbc://{usr}:{pwd}@{adr}:{por}/{sch}?driver=ODBC+Driver+{ver}+for+SQL+Server')

    case default:
        raise "Undefined database engine"

Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()


class DBItem(base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(String)
    price = Column(Float)

    def __str__(self):
        return self.name


class DBSale(base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    customer = Column(String)
    total = Column(Float)
    date = Column(Date)

    items = relationship(DBItem, secondary='sale_details')


class DBSaleDetail(base):
    __tablename__ = 'sale_details'

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('inventory.id'), primary_key=True)
    amount = Column(Integer)


class DBCustomer(base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    identity_card = Column(String)
    address = Column(String)
    insert_date = Column(Date)

    def __str__(self):
        return self.name


base.metadata.create_all(engine)
