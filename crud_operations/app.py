from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pdb

app = Flask(__name__)
app.secret_key = "0C4A94FDA7E81B47EDE8C73BAAF6513F8E9A71D7552ADD966837ED674F36C8E1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/company'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    address = db.Column(db.String(255))
    profile = db.relationship('Account', backref='users', uselist=False)

    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    ifsc_code = db.Column(db.Integer)
    user = db.relationship('User', backref='account', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __init__(self, account_number, bank_name, location, ifsc_code, user_id):
        self.account_number = account_number
        self.bank_name = bank_name
        self.location = location
        self.ifsc_code = ifsc_code
        self.user_id = user_id


# @app.route('/users/<id>/account', methods=['get'])


@app.route('/users/<id>/account', methods=['POST','GET'])
def create_account(id = None):
    if request.method =='POST':
        account_number = request.form['account_number']
        account_number = request.form['bank_name']
        location = request.form['location']
        ifsc_code = request.form['ifsc_code']
        user = User.query.get(id)
        account = Account(account_number, account_number, location, ifsc_code, user.id)
        db.session.add(account)
        db.session.commit()

        flash("Account created successfully !!!")
        return render_template("account.html", user = user)
    else:
        # pdb.set_trace()
        user = User.query.get(id)
        return render_template("account.html", user = user)
        
    

@app.route("/")
def index():
    all_data = User.query.all()
    return render_template("index.html", users = all_data)

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    delete_data = User.query.get(id)
    db.session.delete(delete_data)
    db.session.commit()

    flash("User deleted successfully !!!")
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    # Retrieve the data from the form
    if request.method =='POST':
        # pdb.set_trace()
        update_data = User.query.get(id)
        update_data.name = request.form['name']
        update_data.age = request.form['age']
        update_data.address = request.form['address']

        db.session.commit()
        flash("User updated successfully !!!")
        return redirect(url_for('index'))

@app.route("/insert", methods=["POST"])
def insert_data():
    if request.method =='POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        mydata = User(name, age, address)
        db.session.add(mydata)
        db.session.commit()

        flash("User created successfully !!!")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
# with app.app_context():
#     db.create_all()