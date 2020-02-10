from flask import Flask, render_template, url_for, request, redirect
import psycopg2
import config

app = Flask(__name__)

# PostgreSQL and psycopg2 server
con = psycopg2.connect(dbname='cntUserForm',
                       user='postgres',
                       host='localhost',
                       port='5432',
                       password=config.Config.SERVER_PASSWORD)

# Cursor object to execute SQL statements
cur = con.cursor()



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Generating query that we will use to send to post form data to our database
        insert_table_query = "INSERT INTO %s (email, firstName, lastName, age) VALUES ('%s', '%s', '%s', '%s');" % (
            "userTable", request.form['email'], request.form['firstName'], request.form['lastName'],
            int(request.form['age']))

        try:
            cur.execute(insert_table_query)             # Execute the query to insert user to table
            con.commit()                                #
            return redirect('/')
        except:
            return 'There was an issue adding your user.'


    else:
        cur.execute("SELECT * FROM userTable")          # Select all the items from the database to populate table
        items = cur.fetchall()                          # Fetch all users and store them in a variable called items
        return render_template('index.html', users=items)


@app.route('/delete/<string:email>')
def delete(email):

    # Generating query that we will use to delete a user from the database
    delete_table_query = "DELETE FROM %s WHERE email = '%s';" % (
        "userTable", email)

    try:
        cur.execute(delete_table_query)                 # Execute the query to delete the table entry
        con.commit()                                    # Commit changes to database
        return redirect('/')                            # Refresh the page
    except:
        return 'There was a problem deleting that user.'


if __name__ == '__main__':
    app.run(debug=True)
