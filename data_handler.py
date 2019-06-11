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
            if row['question_id']==id_:
                answer.append(row['message'])
        return answer





#get_all_data()