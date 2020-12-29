import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import *

class SQLFactory():

    def __init__(self):
        self.connection_string = f"postgresql+psycopg2://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_IP}:{PORT}/{DATABASE}"
        self.db = create_engine(self.connection_string)

    # formInfo should be a list
    def saveDataToDatabase(self, formInfo):
        df = pd.DataFrame([formInfo], columns = ["name", "email", "phone", "address1", "address2", "city", "state", "zip"])

        conn = self.db.connect()
        df.columns = [x.lower() for x in df.columns] #lowercase columns
        df.to_sql(TABLE_NAME, con=conn, schema=SCHEMA, if_exists="append", index=False, method="multi")

        return ({"ok": True})