# Hate Crimes & Road Events

The Hate Crimes & Road Events application allows users to explore the Hate Crimes dataset and the 511 NY Events dataset that are listed below.

## Data

1. Hate Crimes by County and Bias Type: Beginning 2010
https://data.ny.gov/Public-Safety/Hate-Crimes-by-County-and-Bias-Type-Beginning-2010/6xda-q7ev

2. 511 NY Events: Beginning 2010
https://data.ny.gov/Transportation/511-NY-Events-Beginning-2010/ah74-pg4w

## Build

Please make sure you have the newest versions of PostgreSQL and Python 3 installed.
To setup the environment, run the following commands in your terminal:

```
psql -U postgres postgres < code/setup.sql
psql -U app_admin app_database < code/schema.sql

pip install -r requirements.txt
```

## Run

To use the application, run the following commands in your terminal:

Load data: `python3 code/load_data.py`
Run application: `python3 code/application.py`
