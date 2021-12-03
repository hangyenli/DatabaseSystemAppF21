import sys
import psycopg2

class Database():

    def __init__(self):
        connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
        self.conn = psycopg2.connect(connection_string)

    def test(self):
        query = "SELECT county, year, type FROM hateCrime LIMIT 10"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            record = cursor.fetchall()
        return record
