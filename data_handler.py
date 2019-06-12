import csv, time
from datetime import datetime


def get_all_data(filename):

    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)

        return [*reader]


def get_answers_by_id(id_):

    list_of_answers = get_all_data('sample_data/answer.csv')

    return [answer for answer in list_of_answers if answer['question_id'] == id_]


def get_post_by_id(id_):

    list_of_questions = get_all_data("sample_data/question.csv")

    for question in list_of_questions:
        if question['id'] == id_:

            return question


def generate_timestamp():

    return int(time.time())


def convert_timestamp(timestamp):

    return datetime.utcfromtimestamp(int(timestamp) + 7200)


def generate_question_id():

    list_of_questions = get_all_data("sample_data/question.csv")

    return int(list_of_questions[-1]['id']) + 1


def make_question_row(title,message):
    return
