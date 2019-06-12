import csv

def get_all_data():
    with open("sample_data/question.csv", "r") as data_file:
        readed_data=csv.DictReader(data_file)
        return [*readed_data]

def get_answers(id_):
    answer=[]
    with open("sample_data/answer.csv", "r") as answer_file:
        readed_answers=csv.DictReader(answer_file)
        for row in readed_answers:
            if row['question_id'] == id_:
                answer.append(row['message'])
        return answer

def get_post_by_id(id_):

    with open("sample_data/question.csv", "r") as data_file:
        data = csv.DictReader(data_file)
        for row in data:
            if row['id'] == id_:
                return row

def make_question_row(title,message):
    return


def write_question(id_):
    pass
