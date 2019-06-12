import csv, time
from datetime import datetime


def get_all_data(filename):

    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)

        return [*reader]


def get_answers_by_id(id_):

    list_of_answers = get_all_data('sample_data/answer.csv')

    result = [answer for answer in list_of_answers if answer['question_id'] == id_]

    for answer in result:
        answer.pop('question_id', None)
        answer['submission_time'] = convert_timestamp(answer['submission_time'])

    return result


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


def write_question(id_, new_line):
    field_names = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    list_of_questions = get_all_data('sample_data/question.csv')
    for i in list_of_questions:
        if i["id"] == id_:
            i["message"] = new_line["message"]


    with open('sample_data/question.csv', "w") as data_file:
        writer = csv.DictWriter(data_file, field_names)
        writer.writeheader()
        for row in list_of_questions:
            writer.writerow(row)

