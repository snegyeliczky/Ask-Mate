from flask import Flask, redirect, render_template, request, session, url_for
import data_handler
import functions

app = Flask(__name__)
app.secret_key = '$2b$12$yxO3U5wrC1QSvVfL3xrLbu'


@app.route('/')
@app.route('/list')
def route_list():
    username = session['username'] if 'username' in session else None

    sort_by = 'submission_time'
    sort_direction = 'DESC'
    if 'sort_by' in request.args and 'sort_direction' in request.args:
        sort_by = request.args['sort_by']
        sort_direction = request.args['sort_direction']

    questions = data_handler.get_all_data('question', sort_by, sort_direction)
    return render_template('list.html', questions=questions, sort_by=sort_by, sort_direction=sort_direction,
                           username=username)


@app.route('/question/<question_id>')
def route_question_by_id(question_id):
    username = session['username'] if 'username' in session else None
    accepted_answer_id = data_handler.get_accepted_answer_id(question_id)

    question = data_handler.get_data_by_question_id('question', question_id)[0]
    answers = data_handler.get_data_by_question_id('answer', question_id)
    return render_template('question.html', question=question, answers=answers, number_of_answers=len(answers),
                           username=username, accepted_answer_id=accepted_answer_id)


@app.route('/question/<question_id>/')
def route_question_view_count(question_id):
    data_handler.increment_view_number(question_id)

    return redirect(f'/question/{question_id}')


@app.route('/add-a-question', methods=['GET', 'POST'])
@functions.login_required
def route_add_question():
    username = session['username'] if 'username' in session else None

    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        if image == "":
            image = None

        data_handler.add_question(title, message, image, username)
        return redirect('/')

    return render_template('add-a-question.html', username=username)


@app.route('/question/<question_id>/edit-a-question', methods=['GET', 'POST'])
@functions.login_required
def route_edit_a_question(question_id):
    question = data_handler.get_data_by_question_id('question', question_id)[0]
    if question['username'] != session['username']:
        return redirect(url_for('route_question_by_id', question_id=question_id))

    if request.method == 'GET':
        return render_template('edit-a-question.html', question=question, username=session['username'])

    message = request.form['message']
    image = request.form['image']
    data_handler.edit_data('question', question_id, message, image)
    return redirect(url_for('route_question_by_id', question_id=question_id))


@app.route('/question/<question_id>/delete')
@functions.login_required
def route_delete_question(question_id):
    question = data_handler.get_data_by_question_id('question', question_id)[0]
    if question['username'] != session['username']:
        return redirect(url_for('route_question_by_id', question_id=question_id))

    data_handler.delete_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
@functions.login_required
def route_add_answer(question_id):
    if request.method == 'GET':
        question = data_handler.get_data_by_question_id('question', question_id)[0]
        return render_template("new-answer.html", question=question, username=session['username'])

    message = request.form['message']
    image = request.form['image']
    if image == "":
        image = None
    username = session['username']

    data_handler.add_answer(question_id, message, image, username)
    return redirect(f"/question/{question_id}")


@app.route('/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
@functions.login_required
def route_edit_answer(question_id, answer_id):
    answer = data_handler.get_answer_by_id(answer_id)[0]
    if answer['username'] != session['username']:
        return redirect(url_for('route_question_by_id', question_id=question_id))

    if request.method == 'GET':
        question = data_handler.get_data_by_question_id('question', question_id)[0]
        return render_template('edit-answer.html', question=question, answer=answer, username=session['username'])

    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        data_handler.edit_data('answer', answer_id, message, image)
        return redirect(f'/question/{question_id}')


@app.route('/<question_id>/<answer_id>/delete')
@functions.login_required
def delete_answer(question_id, answer_id):
    answer = data_handler.get_answer_by_id(answer_id)[0]
    if answer['username'] != session['username']:
        return redirect(url_for('route_question_by_id', question_id=question_id))

    data_handler.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<vote>')
@functions.login_required
def route_question_vote_count(question_id, vote):
    owner_user = data_handler.get_username_by_question_id(question_id)['username']
    username = session['username']
    vote = int(vote)

    reputation_change = data_handler.check_reputation(vote, username, question_id)
    if reputation_change == 'modify':
        if vote == 1:
            modify_vote = 7
        else:
            modify_vote = -7
        data_handler.edit_reputation(modify_vote, 'question', owner_user)
    elif reputation_change == 'GO':
        data_handler.edit_reputation(vote, 'question', owner_user)

    current_vote = data_handler.question_check_user_vote(username, question_id)

    if current_vote is not None and current_vote == vote:
        return redirect(f'/question/{question_id}')

    elif current_vote is not None and current_vote != vote:
        data_handler.update_question_vote(question_id, username, vote)
        data_handler.edit_question_vote_number(question_id, vote*2)
        return redirect(f'/question/{question_id}')

    data_handler.register_question_vote(question_id, username, vote)
    data_handler.edit_question_vote_number(question_id, vote)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/<vote>')
@functions.login_required
def route_answer_vote_count(question_id, answer_id, vote):
    owner_user = data_handler.get_answer_owner(answer_id)
    username = session['username']
    vote = int(vote)

    answer_reputation_check = data_handler.check_answer_reputation(answer_id, username, vote)
    if answer_reputation_check == 'GO':
        data_handler.edit_reputation(vote, 'answer', owner_user)
    elif answer_reputation_check == 'modify':
        if vote == 'True':
            modify_vote = 12
        else:
            modify_vote = -12

        data_handler.edit_reputation(modify_vote, 'answer', owner_user)

    current_vote = data_handler.answer_check_user_vote(username, answer_id)

    if current_vote is not None and current_vote == vote:
        return redirect(f'/question/{question_id}')

    elif current_vote is not None and current_vote != vote:
        data_handler.update_answer_vote(answer_id, username, vote)
        data_handler.edit_answer_vote_number(answer_id, vote * 2)
        return redirect(f'/question/{question_id}')

    data_handler.register_answer_vote(answer_id, username, vote)
    data_handler.edit_answer_vote_number(answer_id, vote)
    return redirect(f'/question/{question_id}')


@app.route('/search')
def search():
    search_part = request.args['search']
    questions = data_handler.search_question(search_part)
    return render_template('list.html', questions=questions)


@app.route("/registration", methods=['GET', 'POST'])
def route_register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if functions.username_exists(username):
        error_message = "The username you entered is already in use"
        return render_template('register.html', error_message=error_message)
    elif password != password2:
        error_message = "The passwords you entered did not match"
        return render_template('register.html', error_message=error_message)
    hash_password = functions.hash_password(password)
    data_handler.register_user(username, hash_password)
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    plain_text_password = request.form['plain_text_password']

    hashed_password = data_handler.get_hashed_password(username)
    if functions.username_exists(username) and functions.verify_password(plain_text_password, hashed_password):
        session['username'] = username
        return redirect("/")

    error_message = 'Invalid username or password'
    return render_template('login.html', error_message=error_message)


@app.route('/logout')
def route_logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/users')
def route_users():
    username = session['username'] if 'username' in session else None

    users = data_handler.get_all_user_attributes()

    return render_template('users.html', users=users, username=username)


@app.route('/user_page/<username>')
def route_user_page(username):
    questions = data_handler.get_questions_data_by_username(username)
    user_attributes = data_handler.get_one_user_attributes(username)
    answers = data_handler.get_answer_data_by_username(username)
    return render_template('user_page.html', questions=questions, user_attributes=user_attributes, answers=answers,
                           username=username, number_of_answers=len(answers), number_of_questions=len(questions))


@app.route('/<question_id>/<answer_id>/accept_answer')
def route_accept_answer(question_id, answer_id):
    question = data_handler.get_data_by_question_id('question', question_id)[0]
    if question['username'] != session['username']:
        return redirect(url_for('route_question_by_id', question_id=question_id))

    data_handler.accept_answer(answer_id)

    answer_owner = data_handler.get_answer_owner(answer_id)
    data_handler.edit_reputation(15, None, answer_owner)

    return redirect(url_for('route_question_by_id', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8001,
        debug=True
    )
