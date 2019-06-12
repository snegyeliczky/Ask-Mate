from flask import Flask, redirect, render_template, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = sorted(data_handler.get_all_data('sample_data/question.csv'),
                       key=lambda item: item['submission_time'], reverse=True)
    for question in questions:
        question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template('list.html', questions=questions)


@app.route('/question/<id_>')
def route_question_by_id(id_):

    answers = data_handler.get_answers_by_id(id_)

    for answer in answers:
        answer.pop('question_id', None)
        answer['submission_time'] = data_handler.convert_timestamp(answer['submission_time'])

    question = data_handler.get_question_by_id(id_)

    question['view_number'] = str(int(question['view_number']) + 1)
    data_handler.write_question(id_, question)

    question['submission_time'] = data_handler.convert_timestamp(question['submission_time'])

    return render_template('question.html', question=question, answers=answers, id_=id_)


@app.route('/add-a-question', methods=['GET', 'POST'])
def route_add_a_question():

    questions = data_handler.get_all_data('sample_data/question.csv')

    if request.method == "POST":

        new_question = {}
        new_question["id"] = data_handler.generate_id('question')
        new_question["submission_time"] = data_handler.generate_timestamp()
        new_question["view_number"] = "0"
        new_question["vote_number"] = "0"
        new_question["title"] = request.form["title"]
        new_question["message"] = request.form["message"]
        new_question["image"] = ""
        data_handler.write_question("", new_question)

        return redirect('/')

    return render_template('add-a-question.html', questions=questions)


@app.route('/question/<question_id>/edit-a-question', methods=['GET', 'POST'])
def route_edit_a_question(question_id):

    question = data_handler.get_question_by_id(question_id)

    if request.method == "POST":
        question['message'] = request.form['message']
        data_handler.write_question(question_id, question)

        return redirect(f'/question/{question_id}')

    return render_template('edit-a-question.html', post=question)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_new_answer(question_id):

    post = data_handler.get_question_by_id(question_id)

    if request.method == "POST":
        new_answer = {'id': data_handler.generate_id('answer'), 'submission_time': data_handler.generate_timestamp(),
                      'vote_number': 0, 'question_id': question_id, 'message': request.form['answer'], 'image': ''}

        data_handler.sandi_answer_writer(new_answer)

        return redirect(f"/question/{question_id}")

    return render_template("new-answer.html", post=post)


@app.route('/question/<id_>/delete', methods=['GET','POST'])
def delete_question(id_):

    existing_questions = data_handler.delete_post_by_id(id_)
    existing_answers = data_handler.delete_answer_by_id(id_)

    data_handler.sandi_data_writer('sample_data/question.csv', existing_questions)
    data_handler.sandi_answer_writer('sample_data/answer.csv', existing_answers)

    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )