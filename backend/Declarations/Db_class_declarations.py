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

"""
Ideal structure:

T ---> Items <--- 
    id
    name
    description
    category
    subcategory
    brand
    stock
    business_cost
    price
    locations
    barcode
    tax
    tags
    supplier
    reorder_at
    minimum
    maximum
    etd (estimated time of delivery)
    curr_early_expiration
    weight
    dimensions
    warranty
    last_update
    inserted_at
    notes
    active

T ---> Items_from_orders <--- 
    id
    id_order
    id_item 
    name
    quantity
    price_unit
    discount
    price_total
    price_net
    from_location
    shipping_address
    shipping_method
    shipping_cost
    shipping_date
    shipping_eta
    shipping_arrival
    shipping_tracking
    returned
    return_reason
    notes
    insert_date
    update_date
    active
    
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
