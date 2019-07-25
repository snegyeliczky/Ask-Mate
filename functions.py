import database_common
from datetime import datetime
import bcrypt
from flask import url_for, session, redirect
from functools import wraps


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def username_exists(cursor, username):
    cursor.execute("""
                    SELECT username FROM users
                    """)
    list_of_all_user_names = [user['username'] for user in cursor.fetchall()]

    return username in list_of_all_user_names


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('route_login'))
    return wrapper
