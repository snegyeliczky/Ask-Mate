from flask import Flask, redirect, render_template, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_data('sample_data/question.csv')

    return render_template('list.html', questions=questions)


@app.route('/question/<id_>')
def route_question_by_id(id_):

    answers = data_handler.get_answers_by_id(id_)
    post = data_handler.get_post_by_id(id_)
    post['submission_time'] = data_handler.convert_timestamp(post['submission_time'])

    return render_template('question.html', post=post, answers=answers, id_=id_)


@app.route('/add-a-question', methods=['GET', 'POST'])
def route_add_a_question():
    questions = data_handler.get_all_data('sample_data/question.csv')
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        return redirect('/')

    return render_template('add-a-question.html', questions=questions)


@app.route('/question/<question_id>/edit-a-question', methods=['GET', 'POST'])
def route_edit_a_question(question_id):
    post = data_handler.get_post_by_id(question_id)

    if request.method == "POST":
        data_handler.write_question(question_id, request.form)

        return redirect(f'/question/{question_id}')

    return render_template('edit-a-question.html', post=post)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_new_answer(question_id):
    post = data_handler.get_post_by_id(question_id)

    if request.method == "POST":
        answer = request.form["answer"]
        return redirect("/")

    return render_template("new-answer.html", post=post)

@app.route('/question/<id_>/delete', methods=['GET','POST'])
def delet_question(id_):
    existing_questions=data_handler.delete_post_by_id(id_)
    print(existing_questions)
    existing_answers=data_handler.delete_answer_by_id(id_)
    data_handler.sandi_data_writer('sample_data/question.csv',existing_questions)
    data_handler.sandi_answer_writer('sample_data/answer.csv',existing_answers)
    return redirect('/')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )