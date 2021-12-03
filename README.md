# Your Project

Summarize your project in one or two sentences

## Data

List specific URLs where your data can be retrieved. 

Anticipate it being downloaded to the `data` directory

1. 511 NY Events: Beginning 2010
https://data.ny.gov/Transportation/511-NY-Events-Beginning-2010/ah74-pg4w

2. Hate Crimes by County and Bias Type: Beginning 2010
https://data.ny.gov/Public-Safety/Hate-Crimes-by-County-and-Bias-Type-Beginning-2010/6xda-q7ev

## Build

List the steps needed to build your application from the terminal. That should include the step needed to install dependencies (including your non-relational datastore).

You should also include the step needed to set up the database and configure your schema. Assume a clean Postgres install.

```
psql -U postgres postgres < code/setup.sql
psql -U app_admin app_database < code/schema.sql

pip install -r requirements.txt
```

## Run

Explain how to run your application from the terminal. That should include the step needed to run the code that loads the data into your database (as well as any additional step needed to load your supporting dataset(s), if you're taking the course at the graduate level). Also be clear about the entry point for your application. If you've created a web application, remember to include a link to the page hosted by your application.

Load data: `python3 code/load_data.py`
Run application: `python3 code/application.py`
