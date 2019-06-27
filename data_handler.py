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
def get_data_by_question_id(cursor, table, item_id):
    column = 'id'
    if table == 'answer':
        column = 'question_id'

    cursor.execute(f"""
                   SELECT * FROM {table}
                   WHERE {column} = %(id)s
                   ORDER BY submission_time
                   """, {'id': item_id})

    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(answer_id)s
                    """, {'answer_id': answer_id})
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def delete_data(cursor, id_):
    cursor.execute("""  
                   DELETE FROM question WHERE id=%(id)s
                   """, {'id': id_})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                   DELETE FROM answer WHERE id=%(answer_id)s
                   """, {'answer_id': answer_id})


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
def edit_question(cursor, table, item_id, message, image):
    cursor.execute(f"""
                    UPDATE {table}
                    SET message = %(message)s, image = %(image)s
                    WHERE id = %(item_id)s
                    """, {'message': message, 'item_id': item_id, 'image': image})


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


@database_common.connection_handler
def search_question(cursor, search_part):
    search_part = search_part.lower()
    search_part = '%'+search_part+'%'
    cursor.execute("""
                    SELECT * FROM question
                    WHERE LOWER(message) LIKE %(search_part)s or LOWER(title) LIKE %(search_part)s
                    """, {'search_part': search_part})
    result = cursor.fetchall()
    return result


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
