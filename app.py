from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to my Watchlist!'

@app.route('/user/<name>')
def user_page(name):
    return f'User {escape(name)}'

@app.route('/test')
def test_url_for():
    # test the url_for() function
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    return 'Test page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)