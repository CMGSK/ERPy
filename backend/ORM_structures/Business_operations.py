from datetime import date

from backend.declarations import db_class_declarations as DB


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

    sale = DB.DBSale(customer=customer_name, total=total, date=date.today())
    session.add(sale)
    session.commit()
    return sale


def add_detail(session, sale, item, amount):
    detail = DB.DBSaleDetail(sale_id=sale, item_id=item, amount=amount)
    session.add(detail)
    session.commit()
    return session
