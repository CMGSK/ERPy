import datetime

from backend.Declarations import Db_class_declarations as DB


def process_sale(session, customer_name, items):
    total = 0.0
    for item in items:
        instance = session.query(DB.DBItem).filter_by(id=item.id).first()
        if instance and item.amount >= instance.amount:
            total += instance.price * item.amount
            instance.amount -= item.amount
            session.commit()
        else:
            raise ValueError(f'Not enough stock of item {instance.id}:{instance.name}')

    sale = DB.DBSale(customer_name=customer_name, total=total, date=datetime.date)
    session.add(sale)
    session.commit()
    return sale

