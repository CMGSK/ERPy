import pandas as pd
from log import Logger
from backend.declarations.db_class_declarations import *


def import_from_xls(file: str) -> bool:
    xls = pd.ExcelFile(file)
    sheets = xls.sheet_names
    for n in sheets:
        try:
            df = xls.parse(sheet_name=n).to_dict()
            match n.lower():
                case 'items':
                    for i in df:
                        o = DBItem(name=i['name'],
                                   description=i['description'],
                                   category=i['category'],
                                   subcategory=i['subcategory'],
                                   brand=i['brand'],
                                   stock=i['stock'],
                                   business_cost=i["business_cost"],
                                   price=i['price'],
                                   locations=i['locations'],
                                   barcode=i['barcode'],
                                   tax=i['tax'],
                                   tags=i['tags'],
                                   supplier=i['supplier'],
                                   reorder_at=i['reorder_at'],
                                   minimum=i['minimum'],
                                   maximum=i['maximum'],
                                   etd=i['etd'],
                                   curr_early_expiration=i['curr_early_expiration'],
                                   weight=i['weight'],
                                   dimensions=i['dimensions'],
                                   warranty=i['warranty'],
                                   last_update=i['last_update'],
                                   inserted_at=i['inserted_at'],
                                   notes=i['notes'],
                                   active=i['active'])
                        o.

        except:
            Logger.debug('Sheet parse error')
