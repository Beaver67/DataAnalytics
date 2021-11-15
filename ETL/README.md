# ETL
 
## Overview

This repo was created to highlight work products with ETL using SSIS and Airflow.

Covid analysis data is taken directly from the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University ( CSSEGISandData / COVID-19 repo https://github.com/CSSEGISandData/COVID-19). 

The data from the Github repo is available in daily csv files (also available in time-series data) that can be downloaded freely from the repo. This data was downloaded daily into a local repo.

## SSIS

An SSIS package was created to process the latest files for importing into a Staging Table (skipping those that were already imported). 

Data was imported into an Azure database.

Once the file(s) have been imported, a stored proc is run to process the data into a format that can be readily used in Business Analytics software such as Tableau or Power BI.

NOTE: The format of the csv files and subsequent data changed from January 2020 until current date. There was some manual cleanup of the data that was necessary.


![SSIS Graph View](beaver67/dataanalytics/assets/SSIS_ETL.png)

## Airflow

Airflow was used to import the same Covid data as the SSIS file. Python was used to do the looping of csv files since Airflow does not loop natively.

Data was imported into a local SQL Server DB housed in a Docker container (beaver67/DevOps/Docker/main/README.md).

![DAG Graph View](assets/CovidAirflow.png)

## Tech Stack

Python 3.9x, Visual Studio with SSIS extension, MS SQL Server 2019, Airflow

## Resources

Apart from the resources in this repo, several online resources are available for further Covid-19 research.

Johns Hopkins Dashboard (Currently cited by most news organizations)
https://coronavirus.jhu.edu/map.html

CDC Covid-19
https://www.cdc.gov/coronavirus/2019-ncov/index.html

WHO Situation Reports
https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports

NCDHHS Covid-19 Response
https://www.ncdhhs.gov/divisions/public-health/covid19

European Commission Coronavirus Response
https://ec.europa.eu/info/live-work-travel-eu/health/coronavirus-response_en

## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Acknowledgements

 - [Readme Templating Tool](https://readme.so)

  
## TODO

- Show screenshots examples of the visuals.


