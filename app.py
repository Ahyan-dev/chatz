from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "!@#$%^&*()"

@app.route("/goTodelete", methods = ['post', 'get'])
def GoTodelete():
    uname=request.args.get('name')
    return redirect(url_for("Delete", name=uname))

@app.route("/signup", methods = ['post', 'get'])
def signup():
    if request.method == "POST" and "username" and "password" and "email" in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        connect = sqlite3.connect('account.db')
        cursor = connect.cursor()
        values = (username, password, email)
        cursor.execute("INSERT INTO user_info VALUES (?,?,?)",values)
        connect.commit()
        connect.close()
        return redirect('/main')
    return render_template('signup.html')

@app.route("/login", methods = ['post', 'get'])
def login():
    user = ""
    password = ""
    email = "empty@gmail.com"
    if request.method == "POST" and "loginUser" in request.form and "loginPassword" in request.form:
        username = request.form.get('loginUser')
        password = request.form.get('loginPassword')
        user = [username, password, email]
        connect = sqlite3.connect('account.db')
        cursor = connect.cursor()
        cursor.execute("INSERT INTO user_info VALUES (?, ?, ?)", user)
        connect.commit()
        connect.close()
        return redirect(url_for('Submit', name=username))
    return render_template('login.html')

@app.route("/main/<name>", methods = ['POST', 'GET'])
def Submit(name):
    typed = ""
    if request.method == "POST" and "textarea" in request.form:
        typed = request.form.get('textarea')
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        conman = sqlite3.connect('history.db')
        curse = conman.cursor()
        data = [(typed)]
        cursor.execute("INSERT INTO submitted_data VALUES (?)", data)
        curse.execute("INSERT INTO history VALUES (?)", data)
        get = cursor.fetchall()
        connect.commit()
        connect.close()
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT ROWID,* FROM submitted_data")
    get = cursor.fetchall()
    connect.commit()
    connect.close()
    return render_template('index.html', messages=get, name=name)

@app.route("/delete/<name>", methods = ['POST', 'GET'])
def Delete(name):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM submitted_data")
    connect.commit()
    connect.close()
    return redirect(url_for('Submit', name=name))

@app.route("/single_delete/<name>", methods = ['POST', 'GET'])
def Single_delete(name):
        line = request.args.get('ROWID')
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute("delete from submitted_data where rowid=(?)", (line,))
        connect.commit()
        return redirect(url_for('Submit', name=name))
if __name__ == "__main__":
    app.run(debug=True,port=5000)
