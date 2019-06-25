import csv
import time
from datetime import datetime
import database_common

QUESTION_TITLE = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_TITLE = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@database_common.connection_handler
def get_all_data(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_data_by_id(cursor, table, column, id_):
    cursor.execute(f"""
                   SELECT * FROM {table}
                   WHERE {column} = %(id)s
                   """, {'id': id_})

    data = cursor.fetchall()
    return data


@database_common.connection_handler
def delete_data(cursor, id_):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id=%(id)s
                    """, {'id': id_})
    answer_ids = cursor.fetchall()
    print(answer_ids)
    for id in answer_ids:
        cursor.execute(""" DELETE FROM comment WHERE answer_id=%(id)s""", {'id': id['id']})
    cursor.execute("""  DELETE FROM comment WHERE question_id=%(id)s""", {'id': id_})
    cursor.execute("""  DELETE FROM answer WHERE question_id=%(id)s""", {'id': id_})
    cursor.execute("""  DELETE FROM question_tag WHERE question_id=%(id)s""", {'id': id_})
    cursor.execute("""  DELETE FROM question WHERE id=%(id)s""", {'id': id_})


@database_common.connection_handler
def add_question(cursor, title, message, image):
    timestamp = generate_timestamp()
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s)
                    """, {'timestamp': timestamp, 'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def add_answer(cursor, question_id, message):
    timestamp = generate_timestamp()
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, null)
                    """, {'timestamp': timestamp, 'title': title, 'message': message})


def edit_data(id_, new_line, filename):

    list_of_data = get_all_data(cursor)

    for i, row in enumerate(list_of_data):
        if row["id"] == id_:
            list_of_data[i] = new_line

    return list_of_data


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(int(timestamp) + 7200)


def generate_id(data_type):
    list_of_data = get_all_data(f"sample_data/{data_type}.csv")

    return int(max([item['id'] for item in list_of_data])) + 1


@database_common.connection_handler
def test(cursor):
    cursor.execute("SELECT * FROM answer")
    result = cursor.fetchall()
    print(result)
