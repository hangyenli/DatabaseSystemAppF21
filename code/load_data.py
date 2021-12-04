import csv
from pymongo import MongoClient


def main():
    client = MongoClient("mongodb://localhost:27017")
    mongo_db = client["app_database"]
    mongo_crime = mongo_db["hateCrime"]
    mongo_crime.drop()

    filename = "data/Hate_Crimes_by_County_and_Bias_Type__Beginning_2010.csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            # parsing each column of a row
            counter = 0
            d = {}
            for col in row:
                d[fields[counter]] = col
                counter += 1
            mongo_crime.insert_one(d)


if __name__ == '__main__':
    main()
