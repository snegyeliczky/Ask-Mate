import csv

def get_all_data():
    with open("sample_data/question.csv", "r") as data_file:
        readed_data=csv.DictReader(data_file)
        return [*readed_data]




#get_all_data()