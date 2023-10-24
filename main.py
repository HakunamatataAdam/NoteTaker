from flask import Flask, flash, g, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
# app
app = Flask(__name__)

DATABASE = 'notetaker.db'

app.config['SECRET_KEY'] = 'uisrth4et485tw6t76t7yf'

# gets the database 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(sql, args=(), one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

# the home page route
@app.route('/')
def index():
    '''takes the notes to the main page'''
    conn = sqlite3.connect("notetaker.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM note")
    results = cur.fetchall()
    print(results)
    conn.close()   

    return render_template("index.html", results=results)

# passes an id to this route- we then query for THIS item and send just that 
# data to a template.
@app.route('/login', methods=["GET", "POST"])
def login():
    # if the user posts a username and password
    if request.method == "POST":
        # get the username and password
        username = request.form['username']
        password = request.form['password']
        # try to find this user in the database- note- just keepin' it simple so usernames must be unique
        sql = "SELECT * FROM user WHERE username = ?"
        user = query_db(sql=sql, args=(username,), one=True)
        if user:
            # check password matches-
            if check_password_hash(user[2], password):
                # Store the username in the session
                session['user'] = user
                flash("Logged in successfully")
            else:
                flash("Password incorrect")
        else:
            flash("Username does not exist")
    # render this template regardles of get/post
    return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # if the user posts from the signup page
    if request.method == "POST":
        # add the new username and hashed password to the database
        username = request.form['username']
        password = request.form['password']
        # hash it with the cool secutiry function
        hashed_password = generate_password_hash(password)
        # write it as a new user to the database
        sql = "INSERT INTO user (username,password) VALUES (?,?)"
        query_db(sql, (username, hashed_password))
        # message flashes exist in the base.html template and give user feedback
        flash("Sign Up Successful")
    return render_template('register.html')

# logout route where it logs the player out
@app.route('/logout')
def logout():
    # clears the username from the session and redirect back to the home page
    session['user'] = None
    return redirect('/')

# create a new note for the user
@app.route('/add', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        '''it create note with a title and body and uses user_id to make it only accessable to the user who created it '''
        cursor = get_db().cursor()
        title = request.form["title"]
        body = request.form["body"]
        user = session["user"]
        '''it inserts into the database'''
        sql = "INSERT INTO note(title, body, time, user_id) VALUES (?,?,?,?)"
        cursor.execute(sql, (title, body, datetime.datetime.now(), user[0]))
        get_db().commit()
    return redirect('/')


# it deletes the note when clicked the delete button
@app.route('/delete', methods=["GET", "POST"])
def delete():
    id = request.form['id']
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM note WHERE id = ?"
    cursor.execute(sql, (id,))
    db.commit()

    return redirect(url_for('index'))

# it feches all the data of a specific note and shows the user when in the note page 
@app.route('/note/<int:id>')
def note(id):
    conn = sqlite3.connect('notetaker.db')
    cur = conn.cursor()
    result = cur.execute(
        """ SELECT id, title, body, time FROM note WHERE id = ?;""",(id,)
    ).fetchone()
    print(result)

    return render_template('note.html', result=result)

# allows the player to edit the note after created the note from a edit bar on the bottom 
@app.route('/edit', methods=["GET", "POST"])
def edit():
    body = request.form.get('body')
    id = int(request.form.get('id'))
    print(body, id)
    conn = sqlite3.connect('notetaker.db')
    cur = conn.cursor()
    '''after editing the note it updates the data in the database and refreshs the page '''
    result = cur.execute('UPDATE note SET body = ? WHERE id=?', (body, id))
    conn.commit()
    return redirect(url_for('note', id=id))

# an error page where it prevent it from breaking site
@app.errorhandler(404)
def error(e):
    """404 Page"""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)