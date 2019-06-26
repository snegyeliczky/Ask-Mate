from flask import Flask, redirect, render_template, request
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

    return render_template('question.html', question=question, answers=answers)


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
        data_handler.edit_question('question', question_id, message)
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
    print(search_part)
    questions = data_handler.search_question(search_part)
    return render_template('list.html', questions=questions)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8022,
        debug=True
    )
