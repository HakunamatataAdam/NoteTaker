from flask import Flask,g, render_template, request, redirect
import sqlite3

#app
app = Flask(__name__)

DATABASE = 'table.db'

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

@app.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':

        cursor = get_db().cursor()
        new_name = request.form["title"]
        new_description = request.form["body"]
        sql = "INSERT INTO note(name, description) VALUES (?,?)"
        cursor.execute(sql,(new_name, new_description))
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

@app.route('/note')
def note():


    return render_template('note.html')

if __name__ == "__main__":
    app.run(debug=True)