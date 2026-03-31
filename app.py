from flask import Flask, render_template, request
import sqlite3
from model import recommend_plan

app = Flask(__name__)

# create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, weight REAL, height REAL, bmi REAL, plan TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        bmi = weight / (height ** 2)
        plan = recommend_plan(bmi)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (weight, height, bmi, plan) VALUES (?, ?, ?, ?)",
                  (weight, height, bmi, plan))
        conn.commit()
        conn.close()

        result = f"BMI: {round(bmi,2)} | Plan: {plan}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)