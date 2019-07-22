from flask import Flask, redirect, render_template, request, session, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    try:
        sort_by = request.args['sort_by']
        sort_direction = request.args['sort_direction']
    except KeyError:
        sort_by = 'submission_time'
        sort_direction = 'DESC'

    questions = data_handler.get_all_data('question', sort_by, sort_direction)
    return render_template('list.html', questions=questions, sort_by=sort_by, sort_direction=sort_direction)


@app.route('/question/<question_id>')
def route_question_by_id(question_id):

    question = data_handler.get_data_by_question_id('question', question_id)[0]
    answers = data_handler.get_data_by_question_id('answer', question_id)

    return render_template('question.html', question=question, answers=answers, number_of_answers=len(answers))


@app.route('/question/<question_id>/')
def route_question_view_count(question_id):
    data_handler.edit_view_number(question_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<vote>')
def route_question_vote_count(question_id, vote):

    data_handler.edit_vote_number('question', question_id, vote)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/<vote>')
def route_answer_vote_count(question_id, answer_id, vote):

    data_handler.edit_vote_number('answer', answer_id, vote)

    return redirect(f'/question/{question_id}')


@app.route('/add-a-question', methods=['GET', 'POST'])
def route_add_question():

    if request.method == "POST":

        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        if image == "":
            image = None

        data_handler.add_question(title, message, image)
        return redirect('/')

    return render_template('add-a-question.html')


@app.route('/question/<question_id>/edit-a-question', methods=['GET', 'POST'])
def route_edit_a_question(question_id):
    question = data_handler.get_data_by_question_id('question', question_id)[0]

    if request.method == "POST":

        message = request.form['message']
        image = request.form['image']
        data_handler.edit_question('question', question_id, message, image)
        return redirect(f'/question/{question_id}')

    return render_template('edit-a-question.html', question=question)


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    data_handler.delete_data(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_add_answer(question_id):
    question = data_handler.get_data_by_question_id('question', question_id)[0]

    if request.method == "POST":

        message = request.form['message']
        image = request.form['image']
        if image == "":
            image = None

        data_handler.add_answer(question_id, message, image)
        return redirect(f"/question/{question_id}")

    return render_template("new-answer.html", question=question)


@app.route('/search')
def search():
    search_part = request.args['search']
    questions = data_handler.search_question(search_part)
    return render_template('list.html', questions=questions)


@app.route('/<question_id>/<answer_id>/delete')
def delete_answer(question_id, answer_id):
    data_handler.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(question_id, answer_id):
    if request.method == 'GET':
        question = data_handler.get_data_by_question_id('question', question_id)[0]
        answer = data_handler.get_answer_by_id(answer_id)[0]
        return render_template('edit-answer.html', question=question, answer=answer)

    if request.method == 'POST':
        message = request.form['message']
        image = request.form['image']
        data_handler.edit_question('answer', answer_id, message, image)
        return redirect(f'/question/{question_id}')


@app.route('/login', methods=['GET', 'POST'])
def route_login(invalid_login=False):
    if request.method == 'GET':
        return render_template('login.html', invalid_login=invalid_login)
    elif request.method == 'POST':
        username = request.form['username']
        plain_text_password = request.form['plain_text_password']
        hashed_password = data_handler.get_hashed_password(username)

        if data_handler.verify_password(plain_text_password, hashed_password):
            session['username'] = username
            return redirect('/')
        else:
            return redirect(url_for('route_login', invalid_login=True))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
