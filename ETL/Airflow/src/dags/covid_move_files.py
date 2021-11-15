import shutil
import os
from datetime import datetime, date, time, timedelta
from dateutil import parser


from projects.covid import process_files_pymssql as pr
from projects.covid import move_files as mv

# - ./src:/opt/airflow/src

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago


def get_filename(input_date):
    # print(input_date)
    return datetime.strptime(input_date.split(".")[0], "%m-%d-%Y")


# def get_oldest_file():
#     files = sorted(os.listdir(path), key=lambda f: get_filename(f))
#     return files[0]


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
}


@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["covid", "Johns Hopkins"],
)
def covid_move_files():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """

    @task()
    def move_covid_files():
        mv.move_covid_files()

    @task()
    def process_files():
        print("starting something @@@@@@@@@")
        pr.loop_through_files()

    @task()
    def cleanup():
        pr.clean_data()

    move_covid_files() >> process_files() >> cleanup()


covid_move_files_dag = covid_move_files()
