# an object of WSGI application
from flask import Flask, redirect, url_for, request, jsonify
import requests
import psycopg2
import uuid
from pymongo import MongoClient



app = Flask(__name__)  # Flask constructor



master = 3000
port = 5000


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


@app.route('/run', methods=['POST'])
def test():
    # handle the POST request
    if request.method == 'POST':
        content = request.json
        # execute todo

        content['todo']
        content['userId']
        db = Database()
        db.run(content['todo'])
        return "ok"


def runServer(port):
    app.run(port=port)


def post(port, route, json):
    r = requests.post('http://localhost:'+str(port)+route, json=json)
    return r


def get(port, route):
    r = requests.get('http://localhost:'+str(port)+route)
    return r



def getSession(userId):
    route = '/getSession/' + userId + '/' + str(port)
    r = get(master, route)
    result = r.json()
    return result['status']




class Database():
    # init the connection for postgres and mongoDB
    def __init__(self):
        connection_string = "host='localhost' dbname='app_database' \
                             user='app_admin' password='admin_password'"
        self.conn = psycopg2.connect(connection_string)
        client = MongoClient("mongodb://localhost:27017")
        mongo_db = client["app_database"]
        self.mongo_conn = mongo_db["hateCrime"]

    # drop the tables for application data, such as user note
    def initApp(self):
        with self.conn.cursor() as cursor:

            cursor.execute("DROP TABLE IF EXISTS localTaskQueue;")
            cursor.execute("DROP TABLE IF EXISTS userNote;")
            cursor.execute("DROP TABLE IF EXISTS userQuery;")
            cursor.execute("DROP TABLE IF EXISTS userAccessedData;")
            cursor.execute("DROP TABLE IF EXISTS users;")

            cursor.execute("CREATE TABLE users (id VARCHAR(36) PRIMARY KEY);")
            cursor.execute("CREATE TABLE userNote (id VARCHAR(36) PRIMARY KEY, \
                                                   userId VARCHAR(36), \
                                                   note VARCHAR(255), \
                            FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE userQuery (id VARCHAR(36) PRIMARY KEY, \
                                                    userId VARCHAR(36), \
                                                    query VARCHAR(1024), \
                            FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE userAccessedData (id VARCHAR(36) PRIMARY KEY, \
                                                           userId VARCHAR(36), \
                                                           accessedTable VARCHAR(255), \
                                                           accessedColumn VARCHAR(255), \
                            FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE );")
            cursor.execute("create table localTaskQueue ( userId             varchar(36), query              varchar(512), timestamp          timestamp default CURRENT_TIMESTAMP,foreign key (userId) references users(id));")


            self.conn.commit()

    # authenticate a user login
    def authUser(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id = %s", (userId,))
            record = cursor.fetchall()
            if len(record) == 0:
                return False
            else:
                return True

    # register a user login
    def addUser(self, userId):
        with self.conn.cursor() as cursor:
            cursor.execute("insert into users values (%s)", (userId,))
            self.conn.commit()

    # create a query history for user, so he can review it later
    def addUserQuery(self, userId, query):
        with self.conn.cursor() as cursor:
            status = getSession(userId)
            query = query.replace("'", "''")
            q = "INSERT INTO userQuery VALUES ('%s', '%s', '%s')" % (str(uuid.uuid4()), userId, query)
            cursor.execute(q)
            if status == 'on':
                #         push to master directly
                post(master, '/addTask', {"query": q, "userId": userId, "address": str(port)})
            else:
                # save it locally
                db = Database()
                db.saveTask(userId, query)
            self.addUserDataAccessed(userId, [('userQuery', 'query'), ('userQuery', 'userId')])
            self.conn.commit()

    # track what table and columns are accessed by user while using the app
    def addUserDataAccessed(self, userId, col_accessed):
        with self.conn.cursor() as cursor:
            status = getSession(userId)

            for col in col_accessed:
                uid = str(uuid.uuid4())
                query = "INSERT INTO userAccessedData VALUES ('%s', '%s', '%s', '%s')" % (uid, userId, col[0], col[1])
                cursor.execute(query)
                if status == 'on':
                    #         push to master directly
                    post(master, '/addTask', {"query": query, "userId": userId, "address": str(port)})
                else:
                    # save it locally
                    self.saveTask(userId, query)

            self.conn.commit()


    # create a user note in the application to help user remember things
    def createNote(self, userId, note):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO userNote VALUES ('%s', '%s', '%s')" % (str(uuid.uuid4()), userId, note)
            cursor.execute(query)
            self.conn.commit()
            return query

    # function to retrieve all user notes
    def fetchNote(self, userId):
        with self.conn.cursor() as cursor:
            query = "SELECT * FROM userNote WHERE userId = '%s'" % (userId,)
            cursor.execute("SELECT * FROM userNote WHERE userId = %s", (userId,))
            self.addUserQuery(userId, query)

            return cursor.fetchall()

    # function to retrieve all user history queries
    def fetchQuery(self, userId):
        with self.conn.cursor() as cursor:
            query = "SELECT * FROM userQuery WHERE userId = '%s'" % (userId,)
            cursor.execute("SELECT * FROM userQuery WHERE userId = %s", (userId,))
            self.addUserQuery(userId, query)
            self.addUserDataAccessed(userId, [('userQuery', 'userId'), ('userQuery', 'query')])
            return cursor.fetchall()

    # function to retrieve all user history for data access
    def fetchDataAccessed(self, userId):
        with self.conn.cursor() as cursor:
            query = "SELECT DISTINCT userId, accessedTable, accessedColumn \
                     FROM userAccessedData WHERE userId = '%s'" % (userId,)
            cursor.execute("SELECT DISTINCT userId, accessedTable, accessedColumn \
                            FROM userAccessedData WHERE userId = %s", (userId,))
            self.addUserQuery(userId, query)
            self.addUserDataAccessed(userId, [('userAccessedData', 'userId'),
                                              ('userAccessedData', 'accessedTable'),
                                              ('userAccessedData', 'accessedColumn')])
            return cursor.fetchall()

    def saveTask(self, userId, query):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO localTaskQueue VALUES (%s, %s)",
                           (userId, query))
            self.conn.commit()
            return

    # function to execute a query in postgres
    def runQuery(self, userId, query, col_accessed):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            # add to user query history
            self.addUserQuery(userId, query)
            # track what data uasge
            self.addUserDataAccessed(userId, col_accessed)
            self.conn.commit()
            return cursor.fetchall()

    def run(self,query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()


    def addTask(self, userId, query):
        #     check if session is on
        status = getSession(userId)

        if status == 'on':
            #         push to master directly
            post(master, '/addTask', {"query": query, "userId": userId, "address": str(port)})
        else:
            # save it locally
            self.saveTask(userId, query)

    # generate a report on hate crime activities
    def getHateCrimeSummary(self):
        counties = []
        # find distinct counties in mongoDB cooltion
        for c in self.mongo_conn.distinct('County'):
            counties.append(c)
        s = ""
        for c in counties[:5]:
            s += c + ', '

        print("Please enter a county name in NY state, such as " + s)
        county = input()

        # run aggregation on mongodb to retrieve the results in the format of
        # county|crime type|total incidents|total victims|total offenders
        ret = list(self.mongo_conn.aggregate([
            {
                "$match": {
                    "County": county,
                    "Crime Type": "Crimes Against Persons"
                }
            },
            {
                "$project":
                    {"Total Incidents": 1, "Total Offenders": 1,
                     "Total Victims": 1, "Year": 1, "County": 1, "_id": 0}
            }
        ]))

        # generate the result table in readable way using the result from the previous step
        counter = 1
        for res in ret:
            s = ""
            s += str(counter) + '. In ' + res['Year'] + ', in county ' + res['County'] + \
                 ' There are ' + res['Total Incidents'] + ' incidents in total, ' + \
                 res['Total Victims'] + ' victims in total, and ' + res['Total Offenders'] + \
                 ' offenders in total'
            print(s)
            counter += 1
