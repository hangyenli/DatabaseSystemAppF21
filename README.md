# Your Project

Summarize your project in one or two sentences

## Data

List specific URLs where your data can be retrieved. 

Anticipate it being downloaded to the `data` directory

## Build

List the steps needed to build your application from the terminal. That should include the step needed to install dependencies (including your non-relational datastore).

You should also include the step needed to set up the database and configure your schema. Assume a clean Postgres install.

Example:

```
psql -U postgres postgres < setup.sql
psql -U myAppAdmin appDatabase < schema.sql

pip install
```

## Run

Explain how to run your application from the terminal. That should include the step needed to run the code that loads the data into your database (as well as any additional step needed to load your supporting dataset(s), if you're taking the course at the graduate level). Also be clear about the entry point for your application. If you've created a web application, remember to include a link to the page hosted by your application.

Example:

Load data: `python3 code/load_data.py`

Run application: `python3 code/application.py`