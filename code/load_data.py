import os
import psycopg2
import pandas as pd

def main():
    connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Load dataset 1
    df_1 = pd.read_csv("data/511_NY_Events__Beginning_2010.csv", \
                       delimiter=',', na_filter=False)
        # TODO

    # Load dataset 2
    df_2 = pd.read_csv("data/Hate_Crimes_by_County_and_Bias_Type__Beginning_2010.csv", \
                       delimiter=',', na_filter=False)
    for row in df_2.values:
        query = "INSERT INTO hateCrime VALUES " + str(tuple(row))
        cursor.execute(query)
    conn.commit()

if __name__ == '__main__':
    main()
