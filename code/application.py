import sys
from database import Database


def print_tuple_3(cols, rows):
    col = "".join(col for col in cols)
    print(col)
    for row in rows:
        print("{}\t{}\t{}".format(row[0][:20], row[1], row[2]))


def print_tuple_2(cols, rows):
    col = "".join(col for col in cols)
    print(col)
    for row in rows:
        print('{}\t{}'.format(row[0][:20], row[1]))


def print_tuple(tuples):
    for t in tuples:
        s = ""
        for col in t:
            s += str(col) + '\t'
        print(s)


def answer_question(userId, option, db):
    if option == "1":
        state = input('Please enter the state you want to look at, such as "NY" "NJ" "CT"  :')
        query = "select state, avg(extract(days from (closetime - createtime))) as avg_duration_day " \
                "from event " \
                "join eventlocation e on e.id = event.eventlocationid " \
                "join eventfacility e2 on e2.id = event.eventfacilityid " \
                "where closetime!= '01/01/2030 01:00:00 PM' " \
                "and (type = 'incident' or type='accident') and state = '" + state + "' " \
                                                                                     "group by state;"
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
    elif option == "3":
        db.getHateCrimeSummary()
        pass
    elif option == "4":
        pass
    elif option == "5":
        year = input("Please enter a year to look at from 2010-2020  :")
        query = "SELECT organization, COUNT(*) FROM event " \
                "WHERE EXTRACT(year FROM createTime) = " + year + \
                "GROUP BY organization " \
                "order by count(*) desc limit 10;"
        result = db.runQuery(userId, query, [('event', 'createtime'), ('event', 'organization')])
        print_tuple_2(['Organization, Count'], result)


def process_request(command, userId):
    DB = Database()
    if command == "1":
        print("\t1. What is the average event duration in STATE?")
        print("\t2. What is the total number of each type of events in YEAR?")
        print("\t3. Give me a summary of hate crimes in County in New York State?")
        print("\t4. What is the ratio of construction events and hate crime incidents?")
        print("\t5. How many events are responded by each organization in YEAR?")
        print("\t6. Quit")

        option = input("Please make a choice (1-6): ")
        if option == '6':
            pass
        else:
            answer_question(userId, option, DB)


    elif command == "2":
        print("Create notes while exploring the project dataset!   :")
        note = input('please enter note, hit return / enter button to finish input  :')
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
        number = input('')
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


def main():
    DB = Database()
    DB.initApp()
    print("Welcome!")
    userId = input("Please enter your user ID: ")

    if not DB.authUser(userId):
        print("Invalid user ID.")
        return

    while (1):
        print("\t1. Explore Datasets")
        print("\t2. Create Notes")
        print("\t3. View Saved Notes")
        print("\t4. View and Reran History Query")
        print("\t5. View Data Accessed")
        print("\t6. Quit")

        command = input("Please make a choice (1-6): ")
        if command == "6":
            break
        else:
            process_request(command, userId)


if __name__ == '__main__':
    main()
