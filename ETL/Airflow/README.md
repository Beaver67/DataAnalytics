
# Covid - Airflow ETL

Using [Apache Airflow](https://airflow.apache.org/) to load Covid data from the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University [Github Repository](https://choosealicense.com/licenses/mit/) 

Mimics the processes used in the [Covid SSIS package](https://github.com/CSSEGISandData/COVID-19) which also uses the Covid data files from CSSE.

- **E**xtracted from csv files and put into a Pandas dataframe
- **T**ransformed into a format (manipulating Pandas df) that is suitable for the MS SQL Server Database table.
- **L**oaded into the MS SQL Server database table.

## Features

- Various Python packages and modules allows for flexibility with different file types and additional processing if file contents change.
- Airflow can be used for any type of scheduling with flexible restarts and error handling.


## Screenshots

DAG Graph View

![DAG Graph View](./assets/img/CovidApacheETL.png)

## Installation 

pip install with requirements.txt

```bash
$ pip install -r requirements.txt
```
    
## Tech Stack

Python 3.9x, Airflow 2.2.x, MS SQL Server 2019

## Run Locally

The Standalone command will initialise the database, make a user,
and start all components for you.
```bash
airflow standalone
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Acknowledgements


 - [Project Structure](https://drivendata.github.io/cookiecutter-data-science/)
 - [Readme Templating Tool](https://readme.so)

  
## TODO

- Run Apache Airflow in Docker (docker-compose and dockerfile have been created).
- Deploy MS SQL Server in the same container as Airflow.
