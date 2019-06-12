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

    return render_template('question.html', post=post, answers=answers)


@app.route('/add-a-question', methods=['GET', 'POST'])
def route_add_a_question():
    questions = data_handler.get_all_data('sample_data/question.csv')
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        return redirect('/')

    return render_template('add-a-question.html', questions=questions)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_new_answer(question_id):
    post = data_handler.get_post_by_id(question_id)

    if request.method == "POST":
        answer = request.form["answer"]
        return redirect("/")

    return render_template("new-answer.html", post=post)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8004,
        debug=True
    )