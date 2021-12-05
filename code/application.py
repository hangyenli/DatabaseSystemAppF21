import sys
from database import Database

def answer_question(option):
    if option == "1":
        pass
    elif option == "2":
        pass
    elif option == "3":
        pass
    elif option == "4":
        pass
    elif option == "5":
        pass


def process_request(command, userId):
    if command == "1":
        print("\t1. What is the average event duration in STATE?")
        print("\t2. What is the total number of each type of events in YEAR?")
        print("\t3. What kind of hate crime occurs the most in STATE?")
        print("\t4. What is the ratio of construction events and hate crime incidents?")
        print("\t5. How many events are responded by each organization in YEAR?")
        option = input("Please make a choice (1-5): ")
        answer_question(option)


    elif command == "2":
        print("Create notes while exploring the project dataset!")
        note = input('please enter note, hit return / enter button to finish input')

        # insert
        DB = Database()
        DB.createNote(userId,note)
    elif command == "3":
        DB = Database()
        print("Here are all your saved Notes!")
        notes = DB.fetchNote(userId)
        counter = 1
        for note in notes:
            print(str(counter) + ". " + note[2])
            counter += 1

    elif command == "4":
        pass
    elif command == "5":
        pass

def main():
    DB = Database()
    
    print("Welcome!")
    userId = input("Please enter your user ID: ")

    if not DB.authUser(userId):
        print("Invalid user ID.")
        return

    while (1):
        print("\t1. Explore Datasets")
        print("\t2. Create Notes")
        print("\t3. View Saved Notes")
        print("\t4. View Query History")
        print("\t5. View Data Accessed")
        print("\t6. Quit")

        command = input("Please make a choice (1-6): ")
        if command == "6":
            break
        else:
            process_request(command, userId)

if __name__ == '__main__':
    main()
