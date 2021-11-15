import shutil
import os
from datetime import datetime, date, time, timedelta
from dateutil import parser


if os.name == "posix":
    srcPath = "/Users/donbranthwaite/zShared/PrivateDevelopment/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"
    destPath = "/Users/donbranthwaite/zShared/Beaver67/DataAnalytics/Docker/ETL/src/projects/covid/data/input/"
    # Path Files
    # srcPath = "/src/projects/covid/data/raw/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"s
    # destPath = "/src/projects/covid/data/input/"
# Docker Files
# srcPath = "/opt/airflow/projects/covid/data/raw/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"
# destPath = "/opt/airflow/projects/covid/data/input/"
else:
    srcPath = "Y:\\zShared\\PrivateDevelopment\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
    destPath = "C:\\zCovid\\Input\\csse_covid_19_data\\csse_covid_19_daily_reports\\"

filelist = os.listdir(srcPath)
# start_date = datetime(2021, 9, 1)
# end_date = datetime(2021, 10, 22)


def move_covid_files():
    end_date = datetime.today()
    start_date = end_date - timedelta(30)

    # Remove any files in dest directory
    for f in os.listdir(destPath):
        os.remove(os.path.join(destPath, f))

    for filename in filelist:
        if filename.split(".")[1] == "csv":
            date_time_obj = parser.parse(filename.split(".")[0])
            if start_date <= date_time_obj <= end_date:
                date_time_obj = parser.parse(filename.split(".")[0])
                # print(date_time_obj)
                shutil.copy(srcPath + filename, destPath + filename)


# move_covid_files()
