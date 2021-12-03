import sys
from database import Database

def main():
    DB = Database()
    
    print("Welcome!")
    userId = input("Please enter your user ID: ")
    userName = input("Please enter your user name: ")

    record = DB.test()
    print(record)

if __name__ == '__main__':
    main()
