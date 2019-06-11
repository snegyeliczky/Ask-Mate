from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/')
def route_list():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8002,
        debug=True
    )