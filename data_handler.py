import database_common
from datetime import datetime


@database_common.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(f"""
                    SELECT * FROM {table}
                    ORDER BY {order_by} {direction}
                    """)

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

    for answer_id in answer_ids:
        cursor.execute(""" DELETE FROM comment WHERE answer_id=%(id)s""", {'id': answer_id['id']})

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
def add_answer(cursor, question_id, message, image):
    timestamp = generate_timestamp()
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                   VALUES (%(timestamp)s, 0, %(question_id)s, %(message)s, %(image)s)
                   """, {'timestamp': timestamp, 'question_id': question_id, 'message': message, 'image': image})


@database_common.connection_handler
def edit_question(cursor, table, item_id, message):
    cursor.execute(f"""
                    UPDATE {table}
                    SET message = %(message)s
                    WHERE id = %(item_id)s
                    """, {'message': message, 'item_id': item_id})


@database_common.connection_handler
def edit_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = (SELECT view_number FROM question
                                      WHERE id = %(question_id)s) + 1
                   WHERE id=%(question_id)s
                   """, {'question_id': question_id})


@database_common.connection_handler
def edit_vote_number(cursor, table, item_id, vote):
    cursor.execute(f"""
                    UPDATE {table}
                    SET vote_number = (SELECT vote_number  FROM {table}
                                       WHERE id = %(item_id)s) + %(vote)s 
                    WHERE id = %(item_id)s
                    """, {'item_id': item_id, 'vote': vote})


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
