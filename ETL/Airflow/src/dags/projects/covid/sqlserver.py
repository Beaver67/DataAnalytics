import pyodbc
from datetime import date
import pandas as pd

from sqlalchemy.engine import url
from sqlalchemy import create_engine

# import sqlalchemy
import urllib

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# def __init__(self, driver, server, port, username, password, database, db):
class SQLLoad:
    def __init__(self, db_settings):
        self.db_settings = db_settings

        self.quoted = urllib.parse.quote_plus(
            "DRIVER={"
            + self.db_settings["driver"]
            + "};SERVER="
            + self.db_settings["server"]
            + ", "
            + self.db_settings["port"]
            + ";DATABASE="
            + self.db_settings["database"]
            + ";UID="
            + self.db_settings["username"]
            + ";PWD="
            + self.db_settings["password"]
        )

        self.engine = self.mssql_engine_setup()
        self.conn = self.engine.raw_connection()

    def mssql_engine_setup(self):
        return create_engine(
            "mssql+pyodbc:///?odbc_connect={}".format(self.quoted),
            fast_executemany=True,
        )

    def postgres_engine_setup(self):
        return create_engine(
            "mssql+pyodbc:///?odbc_connect={}".format(self.quoted),
            fast_executemany=True,
        )

    def df_to_mssql(self, tablename, df):
        df.to_sql(
            name=tablename,
            schema="dbo",
            if_exists="append",
            # con=self.mssql_engine_setup(),
            con=self.engine,
            index=False,
            chunksize=1000,
        )

    def execute_sql(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def get_latest_date(self):
        result = self.conn.execute(
            "SELECT CAST(MAX(Last_Update) AS DATE) as LastUpdate FROM (SELECT Last_Update, COUNT(Last_Update) MyCount FROM DailyDataAllBL GROUP BY Last_Update) as MaxDate    WHERE MyCount > 1000"
        )

        row = result.fetchone()[0]

        return row


def setup_df(csv_file_name):
    df = pd.read_csv(csv_file_name)

    df[
        [
            "Lat",
            "Long_",
            "Confirmed",
            "Deaths",
            "Recovered",
            "Active",
            "Incident_Rate",
            "Case_Fatality_Ratio",
        ]
    ] = df[
        [
            "Lat",
            "Long_",
            "Confirmed",
            "Deaths",
            "Recovered",
            "Active",
            "Incident_Rate",
            "Case_Fatality_Ratio",
        ]
    ].fillna(
        value=0
    )
    df["FIPS"] = df["FIPS"].astype(str)
    df[["Recovered", "Active"]] = df[["Recovered", "Active"]].astype(int)
    df.rename(columns={"Long_": "Long"}, inplace=True)
    df["Last_Update"] = pd.to_datetime(df["Last_Update"]).dt.date

    return df


# def setup_db():
#     df = setup_df(
#         "/Users/donbranthwaite/zShared/Beaver67/DataAnalytics/Docker/ETL/src/data/input/09-05-2021.csv"
#     )

#     db_settings = {
#         "driver": "ODBC Driver 17 for SQL Server",
#         "server": "localhost",
#         "port": "15785",
#         "username": "sa",
#         "password": "Pass@word11",
#         "database": "Covid",
#     }

# sql_run = SQLLoad(db_settings)

# sql_run.df_to_mssql(tablename="dailydatarawsingle2", df=df)

# sql_run.execute_sql("EXEC Test")
# sql_run.execute_sql("DELETE FROM dailydatarawsingle2")
# fred = sql_run.get_latest_date()
# print(fred)


# setup_db()
