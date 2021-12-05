import sys
import psycopg2

class Database():

    def __init__(self):
        connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
        self.conn = psycopg2.connect(connection_string)

    def authUser(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id=%s", (userId, ))
            record = cursor.fetchall()
            if len(record) == 0:
                return False
            else:
                return True
