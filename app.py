from flask import Flask, render_template, url_for, request, session, redirect
import sqlite3 

def register_user_to_db(username, password):
    con = sqlite3.connect('data_user.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users(username,password) values (?,?)', (username, password))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect('data_user.db')
    cur = con.cursor()
    cur.execute('Select username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"

@app.route("/log")
def index():
    return render_template('login.html')
   
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return "Username or Password is wrong!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def portfolio():
    return render_template ("index.html" , nadpis= "Portfolio")

@app.route('/contact')
def contact():
    return render_template ("contact.html")

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         query = request.form['query']
         
         
         with sqlite3.connect("data_query.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO tab (name,addr,query) VALUES (?,?,?)",(nm,addr,query) )
            
            con.commit()
            msg = "Přidal jsem tě do systému"
      except:
         con.rollback()
         msg = "bouhužel někde se vyskytla chybka"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sqlite3.connect("data_query.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from tab")
   
   rows = cur.fetchall()
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
    app.run()