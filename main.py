from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import random
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'summer practicate 2024'
db = SQLAlchemy(app)
 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

menu = [{'name': 'contact', 'url':'contact'}]

@app.route('/contact/', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 5:
            flash('Send message')
        else:
            flash('error message')
    return render_template('contact.html', title='contact', menu=menu)


def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/project')
def project():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT genre FROM films')
    genres = cursor.fetchall()
    conn.close()
    return render_template('project.html', genres=genres)

@app.route('/films', methods=['GET'])
def films():
    genre = request.args.get('genre')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if genre:
        cursor.execute('SELECT * FROM films WHERE genre = ?', (genre,))
    else:
        cursor.execute('SELECT * FROM films')
    
    films = cursor.fetchall()
    conn.close()
    
    if not genre:
        films = [random.choice(films)]
    
    return render_template('films.html', films=films)

if __name__ == '__main__':
    app.run(debug=False )