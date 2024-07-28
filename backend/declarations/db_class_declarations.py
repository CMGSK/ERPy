import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Double, Date, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(Path('../.cfg/.env'))
match engine_selection := os.getenv("DB_ENGINE"):
    case "mysql":
        usr = os.getenv("DB_USER")
        pwd = os.getenv("DB_PASSWORD")
        adr = os.getenv("DB_CON_ADDR")
        por = os.getenv("DB_PORT")
        sch = os.getenv("DB_NAME")
        engine = create_engine(f'mysql+pymysql://{usr}:{pwd}@{adr}:{por}/{sch}', echo=True)

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
        engine = create_engine(f'postgresql://{usr}:{pwd}@{adr}:{por}/{sch}', echo=True)

    case "sqlserver":
        # We may deprecate the ability to connect to MSSQLS because they're a bunch of fucks and
        # drivers are un-fucking-reliable and complicated as hell and will cause more problems than anything else
        usr = os.getenv("DB_USER")
        pwd = os.getenv("DB_PASSWORD")
        adr = os.getenv("DB_CON_ADDR")
        por = os.getenv("DB_PORT")
        sch = os.getenv("DB_NAME")
        ver = os.getenv("DB_MSSQL_VER")
        engine = create_engine(f'mssql+pyodbc://{usr}:{pwd}@{adr}:{por}/{sch}?driver=ODBC+Driver+{ver}+for+SQL+Server',
                               echo=True)

    case default:
        raise "Undefined database engine"

Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()


# TODO: Define the foreign keys and the cascade behaviour


class DBItems(base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    subcategory = Column(String)
    brand = Column(String)
    stock = Column(Integer)
    business_cost = Column(Double)
    price = Column(Double)
    locations = Column(String)
    barcode = Column(String)
    tax = Column(Double)
    tags = Column(String)
    supplier = Column(String)
    reorder_at = Column(Integer)
    minimum = Column(Integer)
    maximum = Column(Integer)
    etd = Column(Date)
    curr_early_expiration = Column(Date)
    weight = Column(Double)
    dimensions = Column(String)
    warranty = Column(Integer)
    last_update = Column(Date)
    inserted_at = Column(Date)
    notes = Column(String)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class DBItemsFromOrders(base):
    __tablename__ = 'items_from_orders'

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer)
    id_item = Column(Integer)
    name = Column(String)
    quantity = Column(Integer)
    price_unit = Column(Double)
    discount = Column(Double)
    price_total = Column(Double)
    price_net = Column(Double)
    from_location = Column(String)
    shipping_address = Column(String)
    shipping_method = Column(String)
    shipping_cost = Column(Double)
    shipping_date = Column(Date)
    shipping_eta = Column(Date)
    shipping_arrival = Column(Date)
    shipping_tracking = Column(String)
    returned = Column(Boolean)
    return_reason = Column(String)
    notes = Column(String)
    insert_date = Column(Date)
    update_date = Column(Date)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class DBOrders(base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    id_customer = Column(Integer)
    id_salesperson = Column(Integer)
    date = Column(Date)
    status = Column(String)
    subtotal = Column(Double)
    discount = Column(Double)
    price_total = Column(Double)
    price_net = Column(Double)
    payment_method = Column(String)
    payment_status = Column(String)
    billing_address = Column(String)
    shipping_address = Column(String)
    shipping_method = Column(String)
    shipping_cost = Column(Double)
    shipping_date = Column(Date)
    shipping_eta = Column(Date)
    shipping_arrival = Column(Date)
    cancelled = Column(Boolean)
    cancel_reason = Column(String)
    notes = Column(String)
    insert_date = Column(Date)
    update_date = Column(Date)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}][EUR {self.price_total}] {self.date} '

    # items = relationship(DBItem, secondary='sale_details')


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

"""
Ideal structure:

T ---> Orders <--- 
    id
    id_customer
    id_salesperson
    date
    status
    subtotal
    discount
    price_total
    price_net
    payment_method
    payment_status
    billing_address
    shipping_address
    shipping_method
    shipping_cost
    shipping_date
    shipping_eta
    shipping_arrival
    cancelled
    cancel_reason
    notes
    insert_date
    update_date
    active
    
T ---> Employees <--- 
    id
    name
    surname
    email
    phone
    email
    address
    city
    cp
    country
    hiring_date
    department
    position
    reports_to
    commission
    total_sales
    total_holidays
    holidays_left
    status
    notes
    update_date
    active
    
T ---> Customers <--- 
    id
    name
    surname
    is_company
    email
    phone
    billing_address
    billing_cp
    shipping_address
    shipping_cp
    shipping_country
    credit_limit
    IBAN
    BIC_SWIFT
    total_sales
    preferred_contact_method
    status
    notes
    insert_date
    update_date
    active
    
T ---> Configurations <--- 
    id
    conf_var
    description
    value
    arguments
    filters
    to_env
    restriction_level
    insert_date
    update_date
    active
    
T ---> Contacts <--- 
    id
    name
    surname
    email
    phone
    position
    department
    company
    relative_to
    notes
    insert_date
    update_date
    
T ---> Storages <--- 
    id
    id_contact
    ref
    location
    storage_address
    storage_city
    storage_cp
    capacity
    status
    notes
    insert_date
    update_date
    active

T ---> Shipments <--- 
    id
    id_order
    id_item
    date
    tracking
    company
    shipping_address
    status
    notes
    insert_date
    update_date
    active
    
T ---> Monetary_transactions <--- 
    id
    id_actor
    time
    date
    ammount_recieved
    actor
    reason
    method
    notes
    insert_date
    update_date
    active
    
T ---> CheckIn <--- 
    id
    id_employee
    timedate_in
    timedate_out
    active
    
T ---> Holidays <--- 
    id
    id_employee
    date_from
    date_to
    hours
    notes
    is_imposed
    is_deductible
    status
    insert_date
    update_date
    active
    
T ---> Internal_code_reports <--- 
    id
    timedate
    message
    metadata
    is_warning
    is_fatal
    active

    
    
"""
