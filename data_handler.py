import csv, time
from datetime import datetime


def get_all_data(filename):

    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)

        return [*reader]


def get_answers_id(id_):

    list_of_answers = get_all_data('sample_data/answer.csv')

    return [answer for answer in list_of_answers if answer['question_id'] == id_]


def get_post_by_id(id_):

    with open("sample_data/question.csv", "r") as data_file:
        data = csv.DictReader(data_file)
        for row in data:
            if row['id'] == id_:
                return row


def generate_timestamp():

    return int(time.time())


def convert_timestamp(timestamp):

    return datetime.utcfromtimestamp(int(timestamp) + 7200)


def generate_question_id():

    list_of_questions = get_all_data()

    return int(list_of_questions[-1]['id']) + 1


def make_question_row(title,message):
    return


print(generate_question_id())