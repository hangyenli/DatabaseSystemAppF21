import sys
from database import Database

address = 'address2'

def print_tuple_3(cols, rows):
    col = "\t\t".join(col for col in cols)
    print(col)
    for row in rows:
        print("{}\t\t{}\t\t{}".format(row[0][:20], row[1], row[2]))


def print_tuple_2(cols, rows):
    col = "\t\t".join(col for col in cols)
    print(col)
    for row in rows:
        print('{}\t\t{}'.format(row[0][:20], row[1]))


def print_tuple(tuples):
    for t in tuples:
        s = ""
        for col in t:
            s += str(col) + '\t'
        print(s)


def answer_question(userId, option, db):
    # question 1
    if option == "1":
        state = input('Please enter the state you want to look at, such as "NY" "NJ" "CT":')
        state = sanitize(state)
        query = "SELECT state, AVG(EXTRACT(days FROM (closetime - createtime))) AS avg_duration_day \
                 FROM event \
                 JOIN eventlocation e ON e.id = event.eventlocationid \
                 JOIN eventfacility e2 ON e2.id = event.eventfacilityid \
                 WHERE closetime!= '01/01/2030 01:00:00 PM' \
                 AND (type = 'incident' OR type = 'accident') \
                 AND state = '" + state + "' group by state;"
        result = db.runQuery(userId, query,
                             [('event', 'createtime'), ('event', 'closetime'), ('eventLocation', 'state'),
                              ('eventFacility', 'type')])
        print("The average length of the event in " + state + " is around " + str(result[0][1]) + 'day(s)')
    elif option == "2":
        # What is the total number of each type of events in YEAR?
        query = "SELECT type as \"Event type\", extract(year from createtime) as year, count(*) " \
                "from event " \
                "join eventfacility e on e.id = event.eventfacilityid " \
                "group by type, extract(year from createtime) having count(*) > 1000 " \
                "order by type, year desc, count(*) desc;"
        result = db.runQuery(userId, query, [('event', 'createtime'), ('eventFacility', 'type')])
        print_tuple_3(["Event Type", "Year", "Count"], result)
        print('-----------------------')
    elif option == "3":
        db.getHateCrimeSummary()
        pass
    elif option == "4":
        query = "select to_char(createtime, 'YYYY') as year, facility, count(*) " \
                "from event " \
                "join eventlocation e on e.id = event.eventlocationid " \
                "join eventfacility e2 on e2.id = event.eventfacilityid " \
                "where (type like '%incident%' or type like '%accident%') " \
                "group by to_char(createtime, 'YYYY'), facility " \
                "having count(*)>1000 " \
                "order by count(*) desc " \
                "limit 20;"
        result = db.runQuery(userId, query,
                             [('event', 'createtime'), ('eventFacility', 'facility'), ('eventLocation', 'county')])
        print_tuple_3(['Year', 'facility', 'count'], result)
        print('-----------------------')

    elif option == "5":
        year = input("Please enter a year to look at from 2010-2020  :")
        year = sanitize(year)
        query = "SELECT organization, COUNT(*) FROM event " \
                "WHERE EXTRACT(year FROM createTime) = " + year + \
                "GROUP BY organization " \
                "order by count(*) desc limit 10;"
        result = db.runQuery(userId, query, [('event', 'createtime'), ('event', 'organization')])
        print_tuple_2(['Organization, Count'], result)


def process_request(command, userId):
    # initiate database connection
    DB = Database()

    # case 1, explore dataset
    if command == "1":
        print("\t1. What is the average event duration in STATE?")
        print("\t2. What is the total number of each type of events in YEAR?")
        print("\t3. Give me a summary of hate crimes in County in New York State?")
        print("\t4. Give me a summary of accident events in New York State")
        print("\t5. How many events are responded by each organization in YEAR?")
        print("\t6. Quit")

        # ask for user input
        option = input("Please make a choice (1-6): ")
        option = sanitize(option)
        # quit program if user wishes to do so
        if option == '6':
            pass
        else:
            # answer corresponding question
            answer_question(userId, option, DB)

    elif command == "2":
        # ask for user input
        print("Create notes while exploring the project dataset!   :")
        note = input('please enter note, hit return / enter button to finish input  :')
        note = sanitize(note)
        DB.createNote(userId, note)

    elif command == "3":
        print("Here are all your saved Notes!")
        notes = DB.fetchNote(userId)
        counter = 1
        for note in notes:
            print(str(counter) + ". " + note[2])
            counter += 1
        print('---------------------')

    elif command == "4":
        print("Here are all your saved Query!")
        queries = DB.fetchQuery(userId)
        counter = 1
        for query in queries:
            print(str(counter) + ". " + query[2])
            counter += 1
        print('---------------------')
        print("To reran a query, enter the number. To quit enter 0")
        # ask for user input
        number = input('')
        number = sanitize(number)

        if number == "0":
            pass
        else:
            result = DB.runQuery(userId, queries[int(number) - 1][2], [])
            print('--------------')
            print('Here is the result of ' + queries[int(number) - 1][2])
            print_tuple(result)
    elif command == "5":
        print("Here are all the unique columns accessed by user: " + userId + "!")
        accesses = DB.fetchDataAccessed(userId)
        counter = 1
        print('Table Accessed\t\tColumn Accessed')
        for access in accesses:
            print(str(counter) + ". " + access[1] + '\t\t' + access[2])
            counter += 1
        print('---------------------')

# replace any ; with injection found to create an error when executing the sql command
def sanitize(input):
    if ';' not in input:
        return input
    else:
        raise



def main():
    # initiate the data base
    DB = Database()
    DB.initApp()
    print("Welcome!")

    # ask user to enter userID
    userId = input("Please enter your user ID: ")
    userId = sanitize(userId)

    # quit the program if user does not exist
    if not DB.authUser(userId):
        print("Invalid user ID.")
        return

    # main loop
    while (1):
        print("\t1. Explore Datasets")
        print("\t2. Create Notes")
        print("\t3. View Saved Notes")
        print("\t4. View and Reran History Query")
        print("\t5. View Data Accessed")
        print("\t6. Quit")

        # ask for user command
        command = input("Please make a choice (1-6): ")
        command = sanitize(command)

        # quit the app if user choose to do so
        if command == "6":
            break
        else:
        # otherwise process the command
            process_request(command, userId)


if __name__ == '__main__':
    # run main function to start the app
    try:
        main()
    except:
        print("Injection found! App is exiting!!!")
