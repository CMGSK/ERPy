import datetime

import sqlalchemy.orm
from sqlalchemy import Column, Integer, Float, Date, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import Db_utils as dbutil

base = declarative_base()
session: sqlalchemy.orm.Session = dbutil.generate_session()
engine: sqlalchemy.engine = dbutil.generate_engine()


class DBUser(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default='USR')
    email = Column(String)
    hash_pwd = Column(String)
    date_added = Column(Date, default=datetime.datetime.utcnow)
    date_modified = Column(Date)
    last_login = Column(Date)
    active = Column(Boolean, default=True)


class DBCustomer(base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String)
    identity_card = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    date_added = Column(Date)
    date_modified = Column(Date)
    is_business = Column(Boolean)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.identity_card}] {self.name}'


class DBItem(base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tags = Column(String)
    reference = Column(String, unique=True)
    stock = Column(Integer, nullable=False)
    price_per_unit = Column(Float)
    date_added = Column(Date, default=datetime.datetime.utcnow)
    date_modified = Column(Date)
    active = Column(Boolean, default=True)

    def __str__(self):
        return f'[{self.reference}] {self.name}'


class DBSale(base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total = Column(Float)
    date = Column(Date)
    online = Column(Boolean)
    location = Column(String)
    finished = Column(Boolean)
    is_complete_return = Column(Boolean, default=False)
    is_partial_return = Column(Boolean, default=False)

    # Relationship
    customer = relationship("DBCustomer", back_populates='sales')
    details = relationship("DBSaleDetail", back_populates='sales')


class DBSaleDetail(base):
    __tablename__ = 'sale_details'

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('inventory.id'), primary_key=True)
    amount = Column(Integer)
    is_return = Column(Boolean, default=False)

    # Relationship
    sale = relationship("DBSale", back_populates='sale_details')
    item = relationship("DBItem", back_populates='sale_details')
    """
    sale_id = n
    items = session.query(DBItem).join(DBSaleDetail).filter(DBSaleDetail.sale_id == sale_id).all()
    ###
    item_id = n
    sales = session.query(DBSale).join(DBSaleDetail).filter(DBSaleDetail.item_id == item_id).all()
    """


class DBExpense(base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    concept = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    unique = Column(Boolean)
    periodicity = Column(Integer)
    active_periodicity = Column(Boolean)


class DBDynamicData(base):
    __tablename__ = 'dynamic_data'

    id = Column(Integer, primary_key=True)
    concept = Column(String, nullable=False)
    description = Column(String)
    value = Column(String)
    parameters = Column(String)
    active = Column(Boolean)
    sensitive = Column(Boolean, default=False)
    prioritize = Column(Boolean, default=False)


base.metadata.create_all(engine)
