import datetime

from backend.Declarations import Db_class_declarations as DB


def add_customer(session, name, identity_card, address):
    try:
        item = DB.DBCustomer(name=name, identity_card=identity_card, address=address, insert_date=datetime.date)
        session.add(item)
        session.commit()
        return item
    except Exception as err:
        return str(err)


def get_all_customers(session):
    return session.query(DB.DBCustomer).all()


def update_customer(session, customer_id, name=None, identity_card=None, address=None):
    item = session.query(DB.DBItem).filter_by(id=customer_id).first()
    if item:
        if name is not None:
            item.customer = name
        if identity_card is not None:
            item.total = identity_card
        if address is not None:
            item.date = address
        session.commit()
    return item


def delete_customer(session, customer_id):
    item = session.query(DB.DBCustomer).filter_by(id=customer_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False
