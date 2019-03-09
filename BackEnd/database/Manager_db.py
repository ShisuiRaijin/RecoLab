import time

from BackEnd.database.common.Base_db import Base_db
from BackEnd.database.common.Stores_db import Stores_DB

class Manager:

    status_db = status_lt = False  # lt = load_tables
    tables = []

    def __init__(self):
        self.db = self.open_database()
        self.load_tables()

    def open_database(self):
        try:
            data_base = Base_db()
        except:
            raise Exception("cant open the database")
        self.status_db = True
        return data_base

    def load_tables(self):

        if self.status_db is False:
            self.open_database()

            if self.status_db is False:
                raise Exception("the data base is down!")

        try:
            stores = Stores_DB(self.db)
            # products = Products_db(self.db) to be implemented

            self.tables.append(stores)
        except:
            return False
        return True

    def get_status(self):
        msg = "Status:  lt = {}, db = {}".format(self.status_lt, self.status_db)
        print(msg)

    def delete_table(self, i):
        del self.tables[i]
