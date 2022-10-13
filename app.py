"""
(5) Initial comments with your name, class and project at the top of your .py file:
INF601 - Advanced Programming in Python
Sam Boutros
Mini Project 3
10/23/2022
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
