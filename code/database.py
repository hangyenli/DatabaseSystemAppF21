import sys
import psycopg2
import uuid


class Database():

    def __init__(self):
        connection_string = "host='localhost' dbname='app_database' user='app_admin' password='admin_password'"
        self.conn = psycopg2.connect(connection_string)

    def initApp(self):
        with self.conn.cursor() as cursor:
            cursor.execute("drop table if exists userNote;")
            cursor.execute("drop table if exists userquery;")
            cursor.execute("drop table if exists userAccesseddata;")
            cursor.execute("drop table if exists users;")

            cursor.execute(" CREATE TABLE users ( id   VARCHAR(36) PRIMARY KEY );")
            cursor.execute(
                " CREATE TABLE userNote ( id     VARCHAR(36) PRIMARY KEY, userId VARCHAR(36), note   VARCHAR(255), FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE );")
            cursor.execute(
                " CREATE TABLE userQuery ( id     VARCHAR(36) PRIMARY KEY, userId VARCHAR(36), query  VARCHAR(1024), FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE);")
            cursor.execute(
                " CREATE TABLE userAccessedData ( id             VARCHAR(36) PRIMARY KEY, userId         VARCHAR(36), accessedTable  VARCHAR(255), accessedColumn VARCHAR(255), FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE );")

            cursor.execute("INSERT INTO users VALUES ('admin')")
            cursor.execute("INSERT INTO users VALUES ('tester')")

            self.conn.commit()

    def authUser(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id=%s", (userId,))
            record = cursor.fetchall()
            if len(record) == 0:
                return False
            else:
                return True

    def addUserQuery(self, userId, query):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into userQuery values (%s,%s,%s)", (str(uuid.uuid4()), userId, query))
            self.addUserDataAccessed(userId, [('userQuery', 'query'), ('userQuery', 'userId')])
            self.conn.commit()

    def addUserDataAccessed(self, userId, col_accessed):
        with self.conn.cursor() as cursor:
            for col in col_accessed:
                query = "insert into userAccessedData values ('%s','%s','%s','%s')" % (
                    str(uuid.uuid4()), userId, col[0], col[1])
                cursor.execute(query)
            self.conn.commit()

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
            self.addUserDataAccessed(userId, [('userQuery', 'userId'), ('userQuery', 'query')])
            return cursor.fetchall()

    def fetchDataAccessed(self, userId):
        with self.conn.cursor() as cursor:
            query = "select distinct userId,accessedTable,accessedColumn from userAccessedData where userId = '%s'" % (
                userId,)
            cursor.execute(query)
            self.addUserQuery(userId, query)
            self.addUserDataAccessed(userId, [('userAccessedData', 'userId'), ('userAccessedData', 'accessedTable'),
                                              ('userAccessedData', 'accessedColumn')])

            return cursor.fetchall()

    def runQuery(self, userId, query, col_accessedd):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.addUserQuery(userId, query)
            self.addUserDataAccessed(userId, col_accessedd)
            self.conn.commit()
            return cursor.fetchall()


