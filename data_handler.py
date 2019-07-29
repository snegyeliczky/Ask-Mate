import database_common
from functions import generate_timestamp


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
def add_question(cursor, title, message, image, username):
    timestamp = generate_timestamp()
    cursor.execute("""
                   INSERT INTO question (submission_time, view_number, vote_number, title, message, image, username)
                   VALUES (%(timestamp)s, 0, 0, %(title)s, %(message)s, %(image)s, %(username)s)
                   """, {'timestamp': timestamp, 'title': title, 'message': message, 'image': image,
                         'username': username})


@database_common.connection_handler
def edit_data(cursor, table, item_id, message, image):
    cursor.execute(f"""
                    UPDATE {table}
                    SET message = %(message)s, image = %(image)s
                    WHERE id = %(item_id)s
                    """, {'message': message, 'item_id': item_id, 'image': image})


@database_common.connection_handler
def delete_question(cursor, id_):
    cursor.execute("""  
                   DELETE FROM question WHERE id=%(id)s
                   """, {'id': id_})


@database_common.connection_handler
def add_answer(cursor, question_id, message, image, username):
    timestamp = generate_timestamp()
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message, image, username)
                   VALUES (%(timestamp)s, 0, %(question_id)s, %(message)s, %(image)s, %(username)s)
                   """, {'timestamp': timestamp, 'question_id': question_id, 'message': message, 'image': image,
                         'username': username})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                   DELETE FROM answer WHERE id=%(answer_id)s
                   """, {'answer_id': answer_id})


@database_common.connection_handler
def increment_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = (SELECT view_number FROM question
                                      WHERE id = %(question_id)s) + 1
                   WHERE id=%(question_id)s
                   """, {'question_id': question_id})


@database_common.connection_handler
def search_question(cursor, search_phrase):
    search_phrase = f'%{search_phrase.lower()}%'
    cursor.execute("""
                   SELECT * FROM question
                   WHERE LOWER(message) LIKE %(search_phrase)s or LOWER(title) LIKE %(search_phrase)s
                   """, {'search_phrase': search_phrase})
    search_result = cursor.fetchall()
    return search_result


@database_common.connection_handler
def get_hashed_password(cursor, username):
    cursor.execute("""
                    SELECT password_hash FROM users
                    WHERE username = %(username)s
                    """, {'username': username})
    hashed_password = cursor.fetchone()
    return hashed_password['password_hash']


@database_common.connection_handler
def register_user(cursor, username, hash_password):
    date = generate_timestamp()
    cursor.execute("""
                    INSERT INTO users
                    VALUES (%(username)s,%(hash_password)s,%(date)s, 0)
                    """, {'username': username, 'hash_password': hash_password, 'date': date})


@database_common.connection_handler
def get_username_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT username
                    FROM question
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id})

    user = cursor.fetchone()
    return user


@database_common.connection_handler
def get_all_user_attributes(cursor):

    cursor.execute("""
                    SELECT * FROM users
                    ORDER BY username
                    """)
    users = cursor.fetchall()

    return users


@database_common.connection_handler
def get_one_user_attributes(cursor, username):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE username = %(username)s
                    """, {'username': username})
    user = cursor.fetchone()

    return user


@database_common.connection_handler
def get_questions_data_by_username(cursor, username):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE username = %(username)s
                    """, {'username': username})
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_answer_data_by_username(cursor, username):
    cursor.execute(f"""
                   SELECT * FROM answer
                   WHERE username = %(username)s
                   ORDER BY submission_time
                   """, {'username': username})

    data = cursor.fetchall()
    return data


@database_common.connection_handler
def accept_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET accepted = TRUE
                    WHERE id = %(answer_id)s
                    """, {'answer_id': answer_id})


@database_common.connection_handler
def get_accepted_answer_id(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id = %(question_id)s and accepted = TRUE
                    """, {'question_id': question_id})

    accepted_ans_id = cursor.fetchone()
    return accepted_ans_id


@database_common.connection_handler
def get_answer_owner(cursor, answer_id):
    cursor.execute(""" 
                    SELECT username
                    FROM answer
                    WHERE id = %(answer_id)s
                    """, {'answer_id': answer_id})

    user = cursor.fetchone()['username']
    return user


@database_common.connection_handler
def edit_reputation(cursor, vote, vote_type, username):
    reputation = vote
    if vote == -1:
        reputation = -2
    elif vote == 1:
        if vote_type == 'question':
            reputation = 5
        elif vote_type == 'answer':
            reputation = 10

    cursor.execute("""
                    UPDATE users
                    SET reputation =
                    (SELECT reputation  FROM users WHERE username = %(username)s)+%(reputation)s
                    WHERE username = %(username)s
                    """, {'username': username, 'reputation': reputation})


@database_common.connection_handler
def check_reputation(cursor, actual_vote, username, question_id):
    cursor.execute("""
                    SELECT vote FROM question_votes
                    WHERE username = %(username)s AND question_id = %(question_id)s
                    """, {'username': username, 'question_id': question_id})
    vote = cursor.fetchone()
    if vote is None:
        return 'GO'
    else:
        vote = vote['vote']
        if vote == actual_vote:
            return None
        else:
            return 'modify'


@database_common.connection_handler
def check_answer_reputation(cursor, question_id, answer_id, username, actual_vote):
    cursor.execute("""
                    SELECT vote
                    FROM answer_votes
                    WHERE question_id= %(question_id)s AND answer_id = %(answer_id)s AND username = %(username)s
                    """, {'question_id': question_id, 'answer_id': answer_id, 'username': username})
    vote = cursor.fetchone()

    if vote is None:
        return 'GO'
    else:
        vote = vote['vote']
        if vote == actual_vote:
            return None
        else:
            return 'modify'


@database_common.connection_handler
def question_check_user_vote(cursor, username, question_id):
    cursor.execute("""
                    SELECT vote FROM question_votes
                    WHERE question_id = %(question_id)s AND username = %(username)s
                    """, {'question_id': question_id, 'username': username})

    result = cursor.fetchone()
    return result['vote'] if result else None


@database_common.connection_handler
def register_question_vote(cursor, question_id, username, vote):

    cursor.execute("""
                   INSERT INTO question_votes
                   VALUES (%(question_id)s, %(username)s, %(vote)s)
                   """, {'question_id': question_id, 'username': username, 'vote': vote})


@database_common.connection_handler
def update_question_vote(cursor, question_id, username, vote):

    cursor.execute("""
                    UPDATE question_votes
                    SET vote = %(vote)s
                    WHERE question_id = %(question_id)s AND username = %(username)s
                    """, {'question_id': question_id, 'username': username, 'vote': vote})


@database_common.connection_handler
def edit_question_vote_number(cursor, question_id, vote):

    cursor.execute("""
                    UPDATE question
                    SET vote_number = (SELECT vote_number FROM question
                                       WHERE id = %(question_id)s) + %(vote)s 
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id, 'vote': vote})









@database_common.connection_handler
def answer_vote_check(cursor, username, vote, question_id, answer_id):
    cursor.execute("""
                    SELECT vote
                    FROM answer_votes
                    WHERE question_id = %(question_id)s AND answer_id = %(answer_id)s AND username = %(username)s
                    """, {'question_id': question_id, 'username': username, 'answer_id': answer_id})
    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
                        INSERT INTO answer_votes
                        VALUES (%(question_id)s, %(answer_id)s, %(username)s, %(vote)s)
                        """, {'question_id': question_id, 'username': username, 'vote': vote, 'answer_id': answer_id})
        return True

    else:
        if result['vote'] == vote:
            return None

        else:
            cursor.execute("""
                            UPDATE answer_votes
                            SET vote = %(vote)s
                            WHERE question_id = %(question_id)s 
                                AND answer_id = %(answer_id)s 
                                AND username = %(username)s
                            """, {'question_id': question_id, 'username': username, 'vote': vote,
                                  'answer_id': answer_id})
            return False
