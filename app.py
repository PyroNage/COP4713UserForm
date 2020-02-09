from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


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
        user_firstName = request.form['firstName']
        user_lastName = request.form['lastName']
        user_email = request.form['email']
        user_age = request.form['age']
        new_user = User(firstName=user_firstName, lastName=user_lastName, email=user_email, age=user_age)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your user.'


    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('index.html', users=users)


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
