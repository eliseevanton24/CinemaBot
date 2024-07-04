from flask import Flask, render_template, request, flash, url_for
import pandas as pd
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'summer practicate 2024'

menu = [{'name': 'contact', 'url':'contact'}]

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/skills', methods=['GET'])
def skills():
    return render_template('skills.html')

@app.route('/contact/', methods = ['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 5:
            flash('Send message')
        else:
            flash('error message')
    return render_template('contact.html', title='contact', menu=menu)

@app.route('/project', methods=['GET'])
def project():
    return render_template('project.html')

# Загрузка данных из CSV-файла
data = pd.read_csv('static/recipes_columnwise.csv')
@app.route('/recipes')
def recipes():
    # Преобразование данных в список словарей для передачи в шаблон
    recipes_list = data.to_dict(orient='records')
    return render_template('recipes.html', recipes=recipes_list)


#@app.route('/films', methods=['GET', 'POST'])
#def films():
#    # Чтение данных из XLSX файла
#    df = pd.read_excel('static/фильмы.xlsx')
#    # Преобразование данных в список словарей для передачи в шаблон
#    data = df.to_dict(orient='records')
#    row = ['Column1']
#    # Отображение данных в HTML-шаблоне
#    return render_template('films.html', data=data, row=row)


@app.route('/films')
def films():
    # Чтение данных из XLSX файла
    df = pd.read_excel('static/фильмы.xlsx')
    # Преобразование данных DataFrame в список словарей для передачи в шаблон'
    row = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5',]
    movies = df.to_dict('records')
    return render_template('index.html', movies=movies, row=row)


if __name__ == '__main__':
    app.run(debug=True)