import csv
import time
from datetime import datetime
QUESTION_TITLE = ["id","submission_time","view_number","vote_number","title","message","image"]
ANSWER_TITLE= ['id','submission_time','vote_number','question_id','message','image']


def get_all_data(filename):

    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)

        return [*reader]


def get_answers_by_id(id_):

    list_of_answers = get_all_data('sample_data/answer.csv')

    return [answer for answer in list_of_answers if answer['question_id'] == id_]


def get_question_by_id(id_):

    list_of_questions = get_all_data("sample_data/question.csv")

    for question in list_of_questions:
        if question['id'] == id_:

            return question


def delete_by_id(id_,filename,id_type='id'):
    posts=get_all_data(filename)
    neaded_posts=[]
    for row in posts:
        if row[id_type]!=id_ :
            neaded_posts.append(row)
    return neaded_posts

def data_writer(filename,to_write,fieldnames):
    with open(filename,"w") as file_to_write:
        writer=csv.DictWriter(file_to_write,fieldnames)
        writer.writeheader()
        for row in to_write:
            writer.writerow(row)

def add_data(new_data,filename):
    list_of_data=get_all_data(filename)
    list_of_data.append(new_data)
    return list_of_data

def edit_data(id_, new_line,filename):

    list_of_data = get_all_data(filename)

    for i, row in enumerate(list_of_data):
        if row["id"] == id_:
            list_of_data[i] = new_line
    return list_of_data


def generate_timestamp():
    return int(time.time())


def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(int(timestamp) + 7200)


def generate_id(type):
    list_of_items = get_all_data(f"sample_data/{type}.csv")
    return int(list_of_items[-1]['id']) + 1

