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
            query = "insert into userNote values ('%s','%s','%s')" % (str(uuid.uuid4()), userId, note)
            cursor.execute(query)
            self.conn.commit()

    def fetchNote(self, userId):
        with self.conn.cursor() as cursor:
            query = "select * from userNote where userId = '%s'" % (userId,)
            cursor.execute(query)
            self.addUserQuery(userId, query)
            return cursor.fetchall()

    def fetchQuery(self, userId):
        with self.conn.cursor() as cursor:
            query = "select * from userQuery where userId = '%s'" % (userId,)
            cursor.execute(query)
            self.addUserQuery(userId, query)
            return cursor.fetchall()


    def addUserQuery(self, userId, query):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into userQuery values (%s,%s,%s)", (str(uuid.uuid4()), userId, query))
            self.conn.commit()

    def runQuery(self, userId, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.addUserQuery(userId, query)
            return cursor.fetchall()


