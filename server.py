from flask import Flask, render_template, redirect, session, request, flash
# import the function connectToMySQL from the file mysqlconnection.py
from mySQLconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "keepItSecretKeepItSafe"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('emailValidation')
# now, we may invoke the query_db method
#print("all the users", mysql.query_db("SELECT * FROM friends;"))

@app.route('/')
def index():
    emails = mysql.query_db("SELECT * FROM emails")
    return render_template('index.html', emails = emails)

@app.route('/success')
def success():
    flash("Success. You have entered your email into our database.")
    emails = mysql.query_db("SELECT * FROM emails")
    return render_template('success.html', emails = emails)

@app.route('/submit', methods=['POST'])
def submit():

    if len(request.form['email']) < 1:
        flash("Entry must not be blank")
        return redirect('/')
    
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address.")
        return redirect('/')

    searchQuery = "SELECT email FROM emails WHERE email = %(email)s;"
    data = { 'email': request.form['email'] }
    alreadyInDB = mysql.query_db(searchQuery, data)

    if alreadyInDB:
        flash("Sign up unsuccessful. Account already exists.")
        return redirect ('/')
    else:
        print("did not find matching email")

        query2 = "INSERT INTO emails (email) VALUES (%(email)s);"
        data = {
                'email': request.form['email']
            }

        mysql.query_db(query2, data)

    return redirect('/success')

@app.route("/delete/<email>")
def delete(email):
    query = "DELETE FROM emails WHERE email = (%(email)s)"
    data = { 'email': email}
    mysql.query_db(query, data)
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)
