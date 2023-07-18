from distutils.util import get_host_platform
from flask import Flask, flash,g, render_template, request, redirect, url_for
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

#app
app = Flask(__name__)

DATABASE = 'notetaker.db'
app.config['SECRET_KEY'] ='uisrth4et485tw6t76t7yf'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/')
def index():
    conn = sqlite3.connect("notetaker.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM note")
    results = cur.fetchall()
    conn.close()
    
    return render_template("index.html", results=results)

@app.route('/add', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':

        cursor = get_db().cursor()
        title = request.form["title"]
        body = request.form["body"]
        time = request.form["time"]
        sql = "INSERT INTO note(title, body, time) VALUES (?,?,?)"
        cursor.execute(sql,(title, body, time))
        get_db().commit()
    return redirect('/')



@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_host_platform(id)

    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, note, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('note.html', post=post)

@app.route('/delete', methods=["GET","POST"])
def delete():
    id = request.form['id']
    db= get_db()
    cursor = db.cursor()
    sql = "DELETE FROM note WHERE id = ?"
    cursor.execute(sql,(id,))
    db.commit()

    return redirect(url_for('index'))

@app.route('/note/<int:id>')
def note(id):
    conn = sqlite3.connect('notetaker.db')
    cur = conn.cursor()
    result=cur.execute(
        """ SELECT body, time, title FROM note WHERE id = ?;""",(id,)
    ).fetchone()
    print(result)

    return render_template('note.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
    