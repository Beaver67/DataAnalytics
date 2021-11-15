# from '~src.etl.sqlserver' import delete_data

import sys

# sys.path.append("../../")

import os
from datetime import date, datetime

# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, "src/dags")

# print(sys.path)

from projects.covid import sqlserver as sr
from projects.covid import move_files as mv

# from projects.covid import file_date as fd

# import sserver as sr

# import move_files as mv
# import file_date as fd
from dateutil import parser
import shutil

# import '~src/etl/sqls/erver'

db_settings = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "localhost",
    "port": "15785",
    "username": "sa",
    "password": "Pass@word11",
    "database": "Covid",
}

# export PYTHONPATH="${PYTHONPATH}:/Users/donbranthwaite/zShared/Beaver67/DataAnalytics/Docker/ETL/"

# path = "/Users/donbranthwaite/zShared/Beaver67/DataAnalytics/Docker/ETL/src/data/input"


def get_filename(input_date):
    # print(input_date)
    return datetime.strptime(input_date.split(".")[0], "%m-%d-%Y")


# def get_oldest_file():
#     files = sorted(os.listdir(path), key=lambda f: get_filename(f))

#     return files[0]


inputPath = "src/projects/covid/data/input/"
archivePath = "src/projects/covid/data/archive/"
errorPath = "src/projects/covid/data/error/"

sql_run = sr.SQLLoad(db_settings)

# Step 1 - Transfer Covid Files
# Move a subsection of the files from the Github repository to the input directory
mv.move_covid_files()


def loop_through_files():
    files = sorted(os.listdir(inputPath), key=lambda f: get_filename(f))
    for file in files:
        sql_run.execute_sql("DELETE FROM dailydatarawsingle")
        compare_dates(file)


# Match Dates to determine next steps
def compare_dates(filename):
    # Step 2 -  Set File Name & extract date
    csv_file_date = parser.parse(filename.split(".")[0]).date()

    # Step 3 - Get Last Update Date from main SQL database
    db_latest_date = sql_run.get_latest_date()

    if db_latest_date == csv_file_date:
        df = sr.setup_df(inputPath + filename)

        print(True, db_latest_date, csv_file_date)
        # Step 4 - LoadLatestCovid File
        sql_run.df_to_mssql(tablename="dailydatarawsingle", df=df)

        # Step 5 - processCovidDaily
        sql_run.execute_sql("EXEC processCovidDaily")

        del df

    else:
        print(False, db_latest_date, csv_file_date)

    shutil.move(inputPath + filename, archivePath + filename)


# loop_through_files()
