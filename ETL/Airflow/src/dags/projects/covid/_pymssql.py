import pymssql
from datetime import date
import pandas as pd


class SQLLoad:
    def __init__(self, db_settings):
        self.db_settings = db_settings

        self.conn = pymssql.connect(
            self.db_settings["server"],
            self.db_settings["username"],
            self.db_settings["password"],
            self.db_settings["database"],
        )

        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        # self.conn.commit()

    def get_latest_date(self):
        self.cursor.execute(
            "SELECT CAST(MAX(Last_Update) AS DATE) as LastUpdate FROM (SELECT Last_Update, COUNT(Last_Update) MyCount FROM DailyDataAllBL GROUP BY Last_Update) as MaxDate    WHERE MyCount > 1000"
        )

        row = self.cursor.fetchone()[0]

        return row

    def load_df(self, df):
        # query = "INSERT INTO dailydatarawsingle (fips, admin2, province_state, country_region, last_update, lat, long, confirmed, deaths, recovered, active, combined_key, incident_rate, case_fatality_ratio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"

        # sql_data = tuple(map(tuple, df.values))
        # print(sql_data)
        # self.cursor.executemany(query, sql_data)

        for index, row in df.iterrows():
            # print(row)
            # sql_data = tuple(map(tuple, row))
            # self.cursor.executemany(query,sql_data)
            self.cursor.execute(
                "INSERT INTO dailydatarawsingle (FIPS, admin2, province_state, country_region, last_update, lat, long, confirmed, deaths, recovered, active, combined_key, incident_rate, case_fatality_ratio) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    row.FIPS,
                    row.Admin2,
                    row.Province_State,
                    row.Country_Region,
                    row.Last_Update,
                    row.Lat,
                    row.Long,
                    row.Confirmed,
                    row.Deaths,
                    row.Recovered,
                    row.Active,
                    row.Combined_Key,
                    row.Incident_Rate,
                    row.Case_Fatality_Ratio,
                ),
            )
        self.conn.commit()

    def load_df_test(self, df):
        # query = "INSERT INTO dailydatarawsingle (fips, admin2, province_state, country_region, last_update, lat, long, confirmed, deaths, recovered, active, combined_key, incident_rate, case_fatality_ratio) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"

        # sql_data = tuple(map(tuple, df.values))
        # print(sql_data)
        # self.cursor.executemany(query, sql_data)

        for index, row in df.iterrows():
            # print(row)
            # sql_data = tuple(map(tuple, row))
            # self.cursor.executemany(query,sql_data)
            query = "INSERT INTO  Test2(ID, Stuff) VALUES(%s,%s)"
            # self.cursor.execute(
            #     "INSERT INTO Test2 (ID, Stuff) VALUES(%s,%s)", (row.ID, row.Stuff)
            # )
            self.cursor.execute(query, ((row.ID), (row.Stuff)))

        self.conn.commit()


# query = ("INSERT INTO  billed_items(item_name,billed_qty,price,item_bill_series) VALUES(%s,%s,%s,%s)")
# c.execute(query,((name),(no),(price),(series))
# conn.commit()


def setup_df(csv_file_name):
    df = pd.read_csv(csv_file_name)

    df[
        [
            "FIPS",
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
            "FIPS",
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

    df[["Admin2", "Province_State",]] = df[["Admin2", "Province_State",]].fillna(
        value=""
    )

    df["FIPS"] = df["FIPS"].astype(int)
    df["FIPS"] = df["FIPS"].astype(str)

    df[["Recovered", "Active"]] = df[["Recovered", "Active"]].astype(int)
    df.rename(columns={"Long_": "Long"}, inplace=True)
    df["Last_Update"] = pd.to_datetime(df["Last_Update"]).dt.date

    return df


def setup_df_test(csv_file_name):
    df = pd.read_csv(csv_file_name)

    return df
