import os
import psycopg2
import pandas as pd
import uuid
import csv
from pymongo import MongoClient

def main():
    # Load dataset 1
    connection_string = "host='localhost' dbname='app_database' \
                         user='app_admin' password='admin_password'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    filename = "data/511_NY_Events__Beginning_2010.csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        # Load eventFacility
        values = set()
        for row in csvreader:
            values.add((row[0], row[2], row[3]))
        params = []
        for value in values:
            param = list(value)
            param.insert(0, str(uuid.uuid4()))
            params.append(tuple(param))
        cursor.executemany("INSERT INTO eventFacility VALUES (%s, %s, %s, %s)",
                           tuple(params))
        conn.commit()

        csvfile.seek(0)
        next(csvreader)
        # Load eventLocation & event
        location_params = []
        event_params = []
        for i, row in enumerate(csvreader):
            # eventLocaation
            location_id = str(uuid.uuid4())
            location_params.append((location_id, row[4], row[5], row[6], row[11], row[12]))
            # event
            cursor.execute("SELECT id FROM eventFacility WHERE type = %s AND \
                           facility = %s AND direction = %s", (row[0], row[2], row[3]))
            facility_id = cursor.fetchall()[0][0]
            event_params.append((str(uuid.uuid4()), row[1], location_id, facility_id, row[7],
                          row[8] if row[8] != '' else '01/01/2030 01:00:00 PM'))

            if i%5000 == 0:
                cursor.executemany("INSERT INTO eventLocation VALUES (%s, %s, %s, %s, %s, %s)",
                                   tuple(location_params))
                cursor.executemany("INSERT INTO event VALUES (%s, %s, %s, %s, %s, %s)",
                                   tuple(event_params))
                location_params = []
                event_params = []
                print(round(i/2627317*100, 2))

        cursor.executemany("INSERT INTO eventLocation VALUES (%s, %s, %s, %s, %s, %s)",
                           tuple(location_params))
        cursor.executemany("INSERT INTO event VALUES (%s, %s, %s, %s, %s, %s)",
                           tuple(event_params))
        conn.commit()

    """
    # Load dataset 2 (non-relational)
    client = MongoClient("mongodb://localhost:27017")
    mongo_db = client["app_database"]
    mongo_crime = mongo_db["hateCrime"]
    mongo_crime.drop()

    filename = "data/Hate_Crimes_by_County_and_Bias_Type__Beginning_2010.csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            # parsing each column of a row
            counter = 0
            d = {}
            for col in row:
                d[fields[counter]] = col
                counter += 1
            mongo_crime.insert_one(d)
    """

if __name__ == '__main__':
    main()
