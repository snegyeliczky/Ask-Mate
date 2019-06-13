from flask import Flask, redirect, render_template, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_data('sample_data/question.csv')
    try:
        if request.args['sort_by'] == 'view_number' or request.args['sort_by'] == 'vote_number':
            sorted_questions = sorted(questions, key=lambda item: int(item[request.args['sort_by']]),
                                      reverse=bool(int(request.args['sort_direction'])))
        else:
            sorted_questions = sorted(questions, key=lambda item: item[request.args['sort_by']],
                                      reverse=bool(int(request.args['sort_direction'])))
    except KeyError:
        sorted_questions = sorted(questions, key=lambda item: item['submission_time'], reverse=True)

    for question in sorted_questions:
        question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template('list.html', questions=sorted_questions)


@app.route('/question/<id_>')
def route_question_by_id(id_):

    answers = data_handler.get_answers_by_id(id_)

    for answer in answers:
        answer.pop('question_id', None)
        answer['submission_time'] = data_handler.convert_timestamp(answer['submission_time'])

    question = data_handler.get_question_by_id(id_)

    question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template('question.html', question=question, answers=answers, id_=id_)


@app.route('/question/<id_>/')
def route_question_view_count(id_):

    question = data_handler.get_question_by_id(id_)
    question['view_number'] = str(int(question['view_number']) + 1)
    final_data=data_handler.edit_data(id_, question, 'sample_data/question.csv')
    data_handler.data_writer('sample_data/question.csv',final_data,data_handler.QUESTION_TITLE)

    return redirect(f'/question/{id_}')


@app.route('/add-a-question', methods=['GET', 'POST'])
def route_add_a_question():

    questions = data_handler.get_all_data('sample_data/question.csv')

    if request.method == "POST":

        new_question = {"id": data_handler.generate_id('question'),
                        "submission_time": data_handler.generate_timestamp(), "view_number": "0", "vote_number": "0",
                        "title": request.form["title"], "message": request.form["message"], "image": ""}

        final_data = data_handler.add_data(new_question, 'sample_data/question.csv')
        data_handler.data_writer('sample_data/question.csv', final_data, data_handler.QUESTION_TITLE)

        return redirect('/')

    return render_template('add-a-question.html', questions=questions)


@app.route('/question/<question_id>/edit-a-question', methods=['GET', 'POST'])
def route_edit_a_question(question_id):
    question = data_handler.get_question_by_id(question_id)

    if request.method == "POST":
        question['message'] = request.form['message']
        final_data=data_handler.edit_data(question_id,question,'sample_data/question.csv')
        data_handler.data_writer('sample_data/question.csv',final_data,data_handler.QUESTION_TITLE)
        return redirect(f'/question/{question_id}')

    return render_template('edit-a-question.html', post=question)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_new_answer(question_id):
    post = data_handler.get_question_by_id(question_id)
    if request.method == "POST":
        new_answer = {'id': data_handler.generate_id('answer'), 'submission_time': data_handler.generate_timestamp(),
                      'vote_number': 0, 'question_id': question_id, 'message': request.form['answer'], 'image': ''}
        final_data=data_handler.add_data(new_answer,'sample_data/answer.csv')
        data_handler.data_writer('sample_data/answer.csv',final_data,data_handler.ANSWER_TITLE)
        return redirect(f"/question/{question_id}")
    return render_template("new-answer.html", post=post)


@app.route('/question/<id_>/delete', methods=['GET','POST'])
def delete_question(id_):

    existing_questions = data_handler.delete_by_id(id_,'sample_data/question.csv')
    existing_answers = data_handler.delete_by_id(id_,'sample_data/answer.csv','question_id')

    data_handler.data_writer('sample_data/question.csv', existing_questions, data_handler.QUESTION_TITLE)
    data_handler.data_writer('sample_data/answer.csv', existing_answers, data_handler.ANSWER_TITLE)

    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )