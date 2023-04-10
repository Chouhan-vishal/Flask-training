from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pdb

''' ==================== Database Configurations ====================== '''

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

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='task')

    def __init__(self, name, description, status, user_id):
        self.name = name
        self.description = description
        self.status = status
        self.user_id = user_id

''' ==================== Account Configurations ====================== '''

@app.route('/users/<id>/account', methods=['POST','GET'])
def create_account(id = None):
    if request.method =='POST':
        account_number = request.form['account_number']
        bank_name = request.form['bank_name']
        location = request.form['location']
        ifsc_code = request.form['ifsc_code']
        user = User.query.get(id)
        account = Account(account_number, bank_name, location, ifsc_code, user.id)
        db.session.add(account)
        db.session.commit()

        flash("Account created successfully !!!")
        return render_template("account.html", user = user)
    else:
        user = User.query.get(id)
        return render_template("account.html", user = user)
    
@app.route('/account/<id>/update', methods=['POST','GET'])
def update_account(id):
    # Retrieve the data from the form
    if request.method =='POST':
        update_data = Account.query.get(id)
        update_data.account_number = request.form['account_number']
        update_data.bank_name = request.form['bank_name']
        update_data.location = request.form['location']
        update_data.ifsc_code = request.form['ifsc_code']

        db.session.commit()
        flash("Account updated successfully !!!")
        return redirect(url_for('index'))


@app.route('/account/<id>/delete', methods=['POST','GET'])
def delete_account(id = None):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    flash("User created successfully !!!")
    return redirect(url_for('index'))

''' ==================== User Configurations ====================== '''

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
    
''' ==================== Tasks Configurations ====================== '''

@app.route("/users/<id>/tasks", methods=['POST','GET'])
def user_tasks(id):
    user = User.query.get(id)
    tasks = Task.query.filter_by(user_id = id).all()
    return render_template("tasks.html", tasks = tasks, user = user)

@app.route("/task/<id>/delete", methods=['POST','GET'])
def task_delete(id):
    task = Task.query.get(id)
    user_id = task.user.id
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully !!!")
    return redirect(url_for('user_tasks', id = user_id))

@app.route("/users/<id>/task", methods=["POST"])
def task_create(id):
    if request.method =='POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        user = User.query.get(id)
        mydata = Task(name, description, status, user.id)
        db.session.add(mydata)
        db.session.commit()

        flash("Task created successfully !!!")
        return redirect(url_for('user_tasks', id = user.id ))

@app.route('/task/<id>/update', methods=['POST','GET'])
def task_update(id):
    # Retrieve the data from the form
    if request.method =='POST':
        update_data = Task.query.get(id)
        update_data.name = request.form['name']
        update_data.description = request.form['description']
        update_data.status = request.form['status']
        user_id = update_data.user.id

        db.session.commit()
        flash("Task updated successfully !!!")
        return redirect(url_for('user_tasks', id = user_id))

''' ==================== Root page Configurations ====================== '''

@app.route("/")
def index():
    all_data = User.query.all()
    return render_template("index.html", users = all_data)

if __name__ == "__main__":
    app.run()
# with app.app_context():
#     db.create_all()