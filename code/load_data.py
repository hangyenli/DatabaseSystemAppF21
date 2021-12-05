import os
import psycopg2
import pandas as pd
import uuid
import csv
from pymongo import MongoClient


def main():
    # Load dataset 1
    connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    df = pd.read_csv("data/511_NY_Events__Beginning_2010.csv", \
                     delimiter=',', na_filter=False)

    cursor.execute
    counter = 0
    for row in df.values:
        # eventLocation
        location_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO eventLocation VALUES " +
                       str((location_id, row[4], row[5], row[6], row[11], row[12])))
        # eventFacility
        cursor.execute("SELECT id FROM eventFacility WHERE type=$$%s$$ AND facility=$$%s$$ AND direction=$$%s$$"
                       % (row[0], row[2], row[3]))
        record = cursor.fetchall()
        facility_id = ""
        if len(record) == 0:
            facility_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO eventFacility VALUES ($$%s$$, $$%s$$,$$%s$$,$$%s$$)" % (
                    facility_id, row[0], row[2], row[3]))
        else:
            facility_id = record[0][0]
        # event


        cursor.execute("INSERT INTO event VALUES ($$%s$$, $$%s$$, $$%s$$,$$%s$$, $$%s$$,$$%s$$)" %
                       (str(uuid.uuid4()), row[1], location_id, facility_id, row[7],
                        row[8] if row[8] != '' else '01/01/2030 01:00:00 PM'))
        counter += 1

        if counter == 5000:
            conn.commit()
            counter = 0

    # Load dataset 2 (Non-relational)
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


if __name__ == '__main__':
    main()
