import csv, time
from datetime import datetime
question_titles=["id","submission_time","view_number","vote_number","title","message","image"]
answer_titles=['id','submission_time','vote_number','question_id','message','image']


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


def delete_post_by_id(id_):
    posts=get_all_data('sample_data/question.csv')
    for row in posts:
        if row['id']==id_:
            posts.remove(row)
    return posts

def delete_answer_by_id(id_):
    posts=get_all_data('sample_data/answer.csv')
    for row in posts:
        if row['question_id']==id_ :
            posts.remove(row)
    return posts

def sandi_data_writer(filename,to_write):
    with open(filename,"w") as file_to_write:
        writer=csv.DictWriter(file_to_write,fieldnames=question_titles)
        writer.writeheader()
        for row in to_write:
            writer.writerow(row)

def sandi_answer_writer(filename,to_write):
    with open(filename,"w") as file_to_write:
        writer=csv.DictWriter(file_to_write,fieldnames=answer_titles)
        writer.writeheader()
        for row in to_write:
            writer.writerow(row)


def generate_timestamp():

    return int(time.time())


def convert_timestamp(timestamp):

    return datetime.utcfromtimestamp(int(timestamp) + 7200)


def generate_question_id():

    list_of_questions = get_all_data("sample_data/question.csv")

    return int(list_of_questions[-1]['id']) + 1


def write_question(id_, new_line):

    field_names = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    list_of_questions = get_all_data('sample_data/question.csv')

    if id_ in [question['id'] for question in list_of_questions]:
        for question in list_of_questions:
            if question["id"] == id_:
                question["message"] = new_line["message"]
    else:
        list_of_questions.append(new_line)

    with open('sample_data/question.csv', "w") as data_file:
        writer = csv.DictWriter(data_file, field_names)
        writer.writeheader()

        for question in list_of_questions:
            writer.writerow(question)

