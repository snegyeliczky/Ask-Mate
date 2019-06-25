from datetime import datetime
import database_common


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
def add_answer(cursor, question_id, message, image):
    timestamp = generate_timestamp()
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(timestamp)s, 0, %(question_id)s, %(message)s, %(image)s)
                    """, {'timestamp': timestamp, 'question_id': question_id, 'message': message, 'image': image})


@database_common.connection_handler
def edit_question(cursor, table, id_, message):
    cursor.execute(f"""
                    UPDATE {table}
                    SET message = %(message)s
                    WHERE id = %(id_)s
                    """, {'message': message, 'id_': id_})

@database_common.connection_handler
def edit_view_number(cursor,question_id):
    cursor.execute("""
                    SELECT view_number FROM question
                    WHERE id = %(question_id)s
                    """, {'question_id':question_id})
    view_number = cursor.fetchall()[0]['view_number']
    view_number += 1
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s
                    WHERE id=%(question_id)s
                    """, {'view_number':view_number, 'question_id':question_id})




def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
