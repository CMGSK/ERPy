from sqlalchemy import create_engine, Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite://erp.db')
session = sessionmaker(bind=engine)
base = declarative_base()


class DBItem(base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


class DBSale(base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    customer = Column(String)
    total = Column(Float)
    date = Column(Date)

    items = relationship('inventory', secondary='sale_details')


class DBSaleDetail(base):
    __tablename__ = 'sale_details'

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('inventory.id'), primary_key=True)
    amount = Column(Integer)


class DBUser(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    identity_card = Column(String)
    address = Column(String)
    insert_date = Column(Date)


base.metadata.create_all(engine)
