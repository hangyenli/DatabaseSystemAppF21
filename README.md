# Hate Crimes & Road Events

The Hate Crimes & Road Events application allows users to explore the Hate Crimes dataset and the 511 NY Events dataset
that are listed below.

## Data

1. Hate Crimes by County and Bias Type: Beginning 2010
   1. Data Source:
      1. https://data.ny.gov/Public-Safety/Hate-Crimes-by-County-and-Bias-Type-Beginning-2010/6xda-q7ev

   2. To download the dataset
      1. Open the link in the previous step
      2. Find export button besides the title
         1. Click on it
         2. Click on CSV button

2. 511 NY Events: Beginning 2010
   1. Data Source
      1. https://data.ny.gov/Transportation/511-NY-Events-Beginning-2010/ah74-pg4w
   2. To download the dataset
      1. Open the link in the previous step
      2. Find export button besides the title
         1. Click on it
         2. Click on CSV button
         3. The dataset is around 500 Mbs
## Requirements

You need to install the python packages specified in the requirements.txt to run this application by running 

```
pip install -r requirements.txt
```

### Notice
You also need to have a MongoDB server running in the localhost at port `27017`

## Build

To setup the environment, run the following commands in your terminal:

```
psql -U postgres postgres < code/setup.sql
psql -U app_admin app_database < code/schema.sql
psql -U app_admin app_database2 < code/schema.sql
```

## Load Data

To load the dataset, run the following commands in your terminal:
```
python3 code/load_data1.py
python3 code/load_data2.py
```

### Notice

The dataset is large, a progress bar will be displayed when loading the dataset. It is ok to interrupt the loading
process by pressing control + c anytime. However, only part of data is loaded.

To load the entire ROad Event dataset. It will take about 10-15 minutes depending on the hardware.


## Run

To run the application, run the following command in the root directory:

```
python3 code/application.py
```
