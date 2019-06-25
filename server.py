from flask import Flask, redirect, render_template, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_data('question')

    try:
        if request.args['sort_by'] == 'view_number' or request.args['sort_by'] == 'vote_number':
            sorted_questions = sorted(questions, key=lambda item: int(item[request.args['sort_by']]),
                                      reverse=bool(int(request.args['sort_direction'])))
        else:
            sorted_questions = sorted(questions, key=lambda item: item[request.args['sort_by']],
                                      reverse=bool(int(request.args['sort_direction'])))

        sort_by = request.args['sort_by']
        sort_direction = request.args['sort_direction']
    except KeyError:
        sorted_questions = sorted(questions, key=lambda item: item['submission_time'], reverse=True)
        sort_by = 'submission_time'
        sort_direction = '1'

    return render_template('list.html', questions=sorted_questions, sort_by=sort_by, sort_direction=sort_direction)


@app.route('/question/<question_id>')
def route_question_by_id(question_id):

    question = data_handler.get_data_by_id('question', 'id', question_id)[0]
    answers = data_handler.get_data_by_id('answer', 'question_id', question_id)

    return render_template('question.html', question=question, answers=answers)


@app.route('/question/<question_id>/')
def route_question_view_count(question_id):

    question = data_handler.get_data_by_id(question_id, 'question')
    question['view_number'] = str(int(question['view_number']) + 1)
    final_data = data_handler.edit_data(question_id, question, 'sample_data/question.csv')
    data_handler.data_writer('sample_data/question.csv', final_data, data_handler.QUESTION_TITLE)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<vote>')
def route_question_vote_count(question_id, vote):

    question = data_handler.get_data_by_id('sample_data/question.csv', question_id)

    question['vote_number'] = str(int(question['vote_number']) + int(vote))
    final_data = data_handler.edit_data(question_id, question, 'sample_data/question.csv')
    data_handler.data_writer('sample_data/question.csv', final_data, data_handler.QUESTION_TITLE)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/<vote>')
def route_answer_vote_count(question_id, answer_id, vote):

    answer = data_handler.get_data_by_id('sample_data/answer.csv', answer_id)

    answer['vote_number'] = str(int(answer['vote_number']) + int(vote))
    final_data = data_handler.edit_data(answer_id, answer, 'sample_data/answer.csv')
    data_handler.data_writer('sample_data/answer.csv', final_data, data_handler.ANSWER_TITLE)

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
    question = data_handler.get_data_by_id('sample_data/question.csv', question_id)

    if request.method == "POST":
        question['message'] = request.form['message']
        final_data = data_handler.edit_data(question_id, question, 'sample_data/question.csv')
        data_handler.data_writer('sample_data/question.csv', final_data, data_handler.QUESTION_TITLE)

        return redirect(f'/question/{question_id}')

    question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template('edit-a-question.html', question=question)


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    data_handler.delete_data(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_add_answer(question_id):
    question = data_handler.get_data_by_id('sample_data/question.csv', question_id)

    if request.method == "POST":
        new_answer = {'id': data_handler.generate_id('answer'), 'submission_time': data_handler.generate_timestamp(),
                      'vote_number': 0, 'question_id': question_id, 'message': request.form['answer'], 'image': ''}
        final_data = data_handler.add_data(new_answer, 'sample_data/answer.csv')
        data_handler.data_writer('sample_data/answer.csv', final_data, data_handler.ANSWER_TITLE)

        return redirect(f"/question/{question_id}")

    question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template("new-answer.html", question=question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8022,
        debug=True
    )
