import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Double, Date, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(Path('../.cfg/.env'))

if os.getenv("DB_ONLINE").lower() == 'true':
    db_mode = 'PROD'
else:
    db_mode = 'LOCAL'

match engine_selection := os.getenv("DB_ENGINE"):
    case "mysql":
        usr = os.getenv(f"DB_{db_mode}_USER")
        pwd = os.getenv(f"DB_{db_mode}_PASSWORD")
        adr = os.getenv(f"DB_{db_mode}_CON_ADDR")
        por = os.getenv(f"DB_{db_mode}_PORT")
        sch = os.getenv(f"DB_{db_mode}_NAME")

        engine = create_engine(f'mysql+pymysql://{usr}:{pwd}@{adr}:{por}/{sch}', echo=True)

    case "sqlite":
        uri = os.getenv(f"DB_{db_mode}_LOCATION")
        sch = os.getenv(f"DB_{db_mode}_NAME")
        engine = create_engine(f'sqlite:///{uri}/{sch}.db', echo=True)

    case "postgresql":
        usr = os.getenv(f"DB_{db_mode}_USER")
        pwd = os.getenv(f"DB_{db_mode}_PASSWORD")
        adr = os.getenv(f"DB_{db_mode}_CON_ADDR")
        por = os.getenv(f"DB_{db_mode}_PORT")
        sch = os.getenv(f"DB_{db_mode}_NAME")
        engine = create_engine(f'postgresql://{usr}:{pwd}@{adr}:{por}/{sch}', echo=True)

    case "sqlserver":
        # We may deprecate the ability to connect to MSSQLS because they're a bunch of fucks and
        # drivers are un-fucking-reliable and complicated as hell and will cause more problems than anything else
        usr = os.getenv(f"DB_{db_mode}_USER")
        pwd = os.getenv(f"DB_{db_mode}_PASSWORD")
        adr = os.getenv(f"DB_{db_mode}_CON_ADDR")
        por = os.getenv(f"DB_{db_mode}_PORT")
        sch = os.getenv(f"DB_{db_mode}_NAME")
        ver = os.getenv(f"DB_{db_mode}_MSSQL_VER")
        engine = create_engine(f'mssql+pyodbc://{usr}:{pwd}@{adr}:{por}/{sch}?driver=ODBC+Driver+{ver}+for+SQL+Server',
                               echo=True)

    case default:
        raise "Undefined database engine"

Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()


# TODO: Define the foreign keys and the cascade behaviour


class DBItem(base):
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

    @classmethod
    def get_all_attr(cls):
        return [k for k in cls.__dict__.keys() if not k.startswith('__')]


class DBItemsFromOrder(base):
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
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class DBOrder(base):
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
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}][EUR {self.price_total}] {self.date} '

    # items = relationship(DBItem, secondary='sale_details')


class DBEmployee(base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    cp = Column(Integer)
    country = Column(Integer)
    hiring_date = Column(Date)
    department = Column(String)
    position = Column(String)
    reports_to = Column(Integer)
    commission = Column(Double)
    total_sales = Column(Integer)
    total_holidays = Column(Integer)
    holidays_left = Column(Integer)
    status = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class DBCustomer(base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    is_company = Column(Boolean)
    email = Column(String)
    phone = Column(String)
    billing_address = Column(String)
    billing_cp = Column(Integer)
    shipping_address = Column(String)
    shipping_cp = Column(Integer)
    shipping_country = Column(String)
    credit_limit = Column(Double)
    IBAN = Column(String)
    BIC_SWIFT = Column(String)
    total_orders = Column(Integer)
    preferred_contact_method = Column(String)
    status = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.name}'


class DBConfiguration(base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    conf_var = Column(String)
    description = Column(String)
    value = Column(String)
    arguments = Column(String)
    filters = Column(String)
    to_env = Column(Boolean)
    restriction_level = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'{self.conf_var}={self.value}'


class DBContact(base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    position = Column(String)
    department = Column(String)
    company = Column(String)
    relative_to = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id} - {self.name}] {self.email} - {self.phone}'


class DBStorage(base):
    __tablename__ = 'storages'

    id = Column(Integer, primary_key=True)
    id_contact = Column(Integer)
    ref = Column(String)
    location = Column(String)
    storage_address = Column(String)
    storage_city = Column(String)
    storage_cp = Column(Integer)
    capacity = Column(String)
    status = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.location}'


class DBShipment(base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer)
    id_item = Column(Integer)
    is_returnal = Column(Boolean)
    date = Column(Date)
    tracking = Column(String)
    company = Column(String)
    shipping_address = Column(String)
    status = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.shipping_address}'


class DBMonetaryTransaction(base):
    __tablename__ = 'monetary_transactions'

    id = Column(Integer, primary_key=True)
    id_actor = Column(Integer)
    time = Column(DateTime)
    ammount = Column(Double)
    actor = Column(String)
    reason = Column(String)
    method = Column(String)
    notes = Column(String)
    insert_date = Column(DateTime)
    update_date = Column(DateTime)
    active = Column(Boolean)

    def __str__(self):
        return f'[{self.id}] {self.actor} - {self.ammount}'


base.metadata.create_all(engine)

"""
Ideal structure:
    
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
    severity
    active

    
    
"""
