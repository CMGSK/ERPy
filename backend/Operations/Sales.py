from backend.Declarations import Db_class_declarations as DB


def add_sale(session, customer, total, date):
    try:
        item = DB.DBSale(customer=customer, total=total, date=date)
        session.add(item)
        session.commit()
        return item
    except Exception as err:
        return str(err)


def get_all_sales(session):
    return session.query(DB.DBSale).all()


def update_sale(session, sale_id, customer=None, total=None, date=None):
    item = session.query(DB.DBItem).filter_by(id=sale_id).first()
    if item:
        if customer is not None:
            item.customer = customer
        if total is not None:
            item.total = total
        if date is not None:
            item.date = date
        session.commit()
    return item


def delete_sale(session, sale_id):
    item = session.query(DB.DBSale).filter_by(id=sale_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False
