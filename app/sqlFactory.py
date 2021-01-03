import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import *
import datetime
import pytz

class SQLFactory():

    def __init__(self):
        self.connection_string = f"sqlite:///{DATABASE}.sqlite"
        self.db = create_engine(self.connection_string)

    # formInfo should be a list
    def saveDataToDatabase(self, formInfo):
        #get id
        new_id = self.getNewID()
        formInfo.insert(0, new_id)

        df = pd.DataFrame([formInfo], columns = ["id", "name", "email", "phone", "address1", "address2", "city", "state", "zip", "country"])
        tz = pytz.timezone('America/Chicago')
        df["last_updated"] = datetime.datetime.now(tz)

        conn = self.db.connect()
        df.columns = [x.lower() for x in df.columns] #lowercase columns
        df.to_sql(TABLE_NAME, con=conn, if_exists="append", index=False, method="multi")

        return ({"ok": True})

    def getNewID(self):
        query = f"""
                    SELECT
                        id
                    from
                        {TABLE_NAME}
                    order by id desc
                    LIMIT 1
                """
        
        old_id = 0
        try:
            conn = self.db.connect()
            df = pd.read_sql(query, con=conn)
            conn.close()

            #table exists but is empty
            old_id = df["id"][0] if len(df) > 0 else 0
        except Exception as e:
            # table doesn't exist
            old_id = 0

        new_id = old_id + 1
        return new_id

    def getAllData(self):
        query = f"""
                    SELECT
                        *
                    from
                        {TABLE_NAME}
                    where
                        name <> ''
                    order by id desc
                """

        conn = self.db.connect()
        df = pd.read_sql(query, con=conn)
        conn.close()

        if len(df) > 0:
            df["last_updated"] = pd.to_datetime(df["last_updated"])
            df["last_updated"] = [x.strftime("%m/%d/%Y %I:%M%p") for x in df.last_updated]
        return (df)