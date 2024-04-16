from backend.Declarations import Db_class_declarations as DB


def add_item(session, name, amount, price):
    try:
        item = DB.DBItem(name=name, amount=amount, price=price)
        session.add(item)
        session.commit()
        return item
    except Exception as e:
        return str(e)


def get_all_items(session):
    return session.query(DB.DBItem).all()


def update_item(session, item_id, name=None, amount=None, price=None):
    item = session.query(DB.DBItem).filter_by(id=item_id).first()
    if item:
        if name is not None:
            item.name = name
        if amount is not None:
            item.amount = amount
        if price is not None:
            item.price = price
        session.commit()
    return item


def delete_item(session, item_id):
    item = session.query(DB.DBItem).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
        return True
    return False