from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS routes
             (id INTEGER PRIMARY KEY, start_point TEXT, end_point TEXT, calories REAL, steps INTEGER)''')
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_point = request.form['start_point']
        end_point = request.form['end_point']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT calories, steps FROM routes WHERE start_point=? AND end_point=?", (start_point, end_point))
        result = c.fetchone()
        conn.close()
        if result:
            calories = result[0]
            steps = result[1]
            return render_template('stepburner.html', calories=calories, steps=steps)
        else:
            return render_template('stepburner.html', error="Route not found")
    return render_template('stepburner.html')

if __name__ == '__main__':
    app.run(debug=True)