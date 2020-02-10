from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)

# SQLAlchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# PostgreSQL and psycopg2 server
con = psycopg2.connect(dbname='cntUserForm',
                       user='postgres',
                       host='localhost',
                       port='5432',
                       password='Postgres011235813')

# Cursor object to execute SQL statements
cur = con.cursor()

# cur.execute(create_Table)
# cur.execute(insert_Table)

con.commit()


class User(db.Model):
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.email


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form['email'], request.form['firstName'], request.form['lastName'], request.form['age'])

        print(type(request.form['age']))

        insert_table_query = '''INSERT INTO userTable (EMAIL, FIRSTNAME, LASTNAME, AGE)
        VALUES (request.form['email'], request.form['firstName'], request.form['lastName'], request.form['age']);'''

        insert_table_query2 = "INSERT INTO %s (email, firstName, lastName, age) VALUES ('%s', '%s', '%s', '%s');" % (
        "userTable", request.form['email'], request.form['firstName'], request.form['lastName'],
        int(request.form['age']))

        print(insert_table_query2)

        try:
            cur.execute(insert_table_query2)
            con.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your user.'


    else:
        cur.execute("SELECT * FROM userTable")
        items = cur.fetchall()
        print("Items from database: ", items)
        return render_template('index.html', users=items)


@app.route('/delete/<string:email>')
def delete(email):
    user_to_delete = User.query.get_or_404(email)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that user.'


if __name__ == '__main__':
    app.run(debug=True)
