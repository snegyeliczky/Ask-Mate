from flask import Flask, redirect, render_template
import data_handler

app = Flask(__name__)


@app.route('/')
def route_list():
    questions=data_handler.get_all_data()

    return render_template('index.html', questions=questions)

@app.route('/<id_>')
def route_answer(id_):
    answer=data_handler.get_answers(id_)

    return render_template("answer.html", answer=answer)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8004,
        debug=True
    )