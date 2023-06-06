from flask import Flask,g, render_template, request, redirect, url_for
import sqlite3

#app
app = Flask(__name__)

DATABASE = 'notetaker.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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

         # Get the data from the form
      #   title = request.form['title']
      #   content = request.form['body']

         # Store the note in the database
      #   get_db.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
      #   get_db.commit()

         # Redirect the user to the homepage
      #   return redirect('/')
  #  else:
         # Display the create note form
    #     return render_template("'A.html'")

@app.route('/note/<int:id>')
def note(id):
    conn = sqlite3.connect('notetaker.db')
    cur = conn.cursor()
    result=cur.execute(
        """ SELECT body, time, title FROM note WHERE id = ?;""",(id,)
    ).fetchone()
    print(result)

    return render_template('note.html', result=result)


@app.route('/delete', methods=["GET","POST"])
def delete():
    id = request.form['id']
    db= get_db()
    cursor = db.cursor()
    sql = "DELETE FROM note WHERE id = ?"
    cursor.execute(sql,(id,))
    db.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)