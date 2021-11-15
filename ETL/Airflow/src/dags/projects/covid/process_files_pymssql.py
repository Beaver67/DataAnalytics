# Use to setup path so that we can import python modules
# export PYTHONPATH="${PYTHONPATH}:/Users/donbranthwaite/zShared/Beaver67/DataAnalytics/Docker/ETL/"

import os
from datetime import date, datetime

from projects.covid import _pymssql as sr
from projects.covid import move_files as mv

from dateutil import parser
import shutil

db_settings = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "localhost",
    "port": "1433",
    "username": "sa",
    "password": "Pass@word11",
    "database": "Covid",
}


def get_filename(input_date):
    # print(input_date)
    return datetime.strptime(input_date.split(".")[0], "%m-%d-%Y")


inputPath = "src/projects/covid/data/input/"
archivePath = "src/projects/covid/data/archive/"
errorPath = "src/projects/covid/data/error/"

sql_run = sr.SQLLoad(db_settings)


def loop_through_files():
    files = sorted(os.listdir(inputPath), key=lambda f: get_filename(f))
    for file in files:
        sql_run.execute_sql("DELETE FROM dailydatarawsingle")
        compare_dates(file)


# Match Dates to determine next steps
def compare_dates(filename):
    # Step 2 -  Set File Name & extract date
    csv_file_date = parser.parse(filename.split(".")[0]).date()
    print(filename)

    # Step 3 - Get Last Update Date from main SQL database
    db_latest_date = sql_run.get_latest_date()

    if db_latest_date == csv_file_date:
        df = sr.setup_df(inputPath + filename)

        print(True, db_latest_date, csv_file_date)
        # Step 4 - LoadLatestCovid File
        # sql_run.df_to_mssql(tablename="dailydatarawsingle", df=df)
        sql_run.load_df(df)

        # Step 5 - processCovidDaily
        sql_run.execute_sql("EXEC processCovidDaily")

        del df

    else:
        print(False, db_latest_date, csv_file_date)

    shutil.move(inputPath + filename, archivePath + filename)


def clean_data():
    sql_run.execute_sql("EXEC Cleanup")


# loop_through_files()
