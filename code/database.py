import sys
import psycopg2
import uuid


class Database():

    def __init__(self):
        connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
        self.conn = psycopg2.connect(connection_string)

    def authUser(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id=%s", (userId,))
            record = cursor.fetchall()
            if len(record) == 0:
                return False
            else:
                return True

    def createNote(self, userId, note):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into userNote ('%s','%s','%s')", (str(uuid.uuid4()), userId, note))
            self.conn.commit()
            return cursor.fetchone()[0]

    def fetchNote(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("select * from userNote where userId = '%s'", (userId,))
            return cursor.fetchall()

    def addUserQuery(self, userId, query):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into userQuery ('%s','%s','%s')", (str(uuid.uuid4()), userId, query))
            self.conn.commit()
            return cursor.fetchone()[0]

    def runQuery(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

