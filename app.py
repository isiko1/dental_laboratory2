import os
from flask import (Flask, render_template,
                   redirect, request, session, url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
# ---------------------------------------Login----------------------------


@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.confirm_password.data == form.password.data:
            flash('Logged in as {}!'.format(form.username.data), 'success')
            return redirect(url_for('get_patients'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    return render_template('login.html', title='Sign In', form=form)
# -----------------------------Register-------------------------------------


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
# ------------Dictionary----------------------------------------------------
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower()
            }
        mongo.db.users.insert_one(register)
# put new user into session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
    return render_template('register.html')
# -----------------------------Read-------------------------------------


@app.route('/get_patients')
def get_patients():
    return render_template('patients.html', patients=mongo.db.patients.find(),
                           type=mongo.db.patients.find())


# -----------------------------Create-------------------------------------
@app.route('/add_patient')
def add_patient():
    return render_template('addpatient.html', jobs=mongo.db.jobs.find(),
                           type=mongo.db.type.find())


@app.route('/insert_patient', methods=["POST"])
def insert_patient():
    patients = mongo.db.patients
    patients.insert_one(request.form.to_dict())
    return redirect(url_for('get_patients'))
# -----------------------------Update---------------------------------


@app.route('/edit_patient/<patient_id>')
def edit_patient(patient_id):
    the_patient = mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
    all_jobs = mongo.db.jobs.find()
    all_type = mongo.db.type.find()
    return render_template('editpatient.html', patient=the_patient,
                           jobs=all_jobs, type=all_type)


@app.route('/update_patient/<patient_id>', methods=["POST"])
def update_patient(patient_id):
    patients = mongo.db.patients
    patients.update({'_id': ObjectId(patient_id)},
                    {'patient_name': request.form.get('patient_name'),
                    'patient_dob': request.form.get('patient_dob'),
                     'gender': request.form.get('gender'),
                     'type_patient': request.form.get('type_patient'),
                        'due_date': request.form.get('due_date'),
                        'job_name': request.form.get('job_name'),
                        'is_urgent': request.form.get('is_urgent')})
    return redirect(url_for('get_patients'))


# -------------------------------Delete---------------------------------
@app.route('/delete_patient/<patient_id>')
def delete_patient(patient_id):
    mongo.db.patients.remove({'_id': ObjectId(patient_id)})
    return redirect(url_for('get_patients'))


# -------------------------------Read-----------------------------------
@app.route('/get_jobs')
def get_jobs():
    return render_template('jobs.html', jobs=mongo.db.jobs.find())


# ------------------------------Update----------------------------------
@app.route('/edit_job/<job_id>')
def edit_job(job_id):
    return render_template('editjob.html',
                           job=mongo.db.jobs.find_one(
                            {'_id': ObjectId(job_id)}))


@app.route('/update_job/<job_id>', methods=["POST"])
def update_job(job_id):
    mongo.db.jobs.update({'_id': ObjectId(job_id)},
                         {'job_name': request.form.get('job_name')})
    return redirect(url_for('get_jobs'))


# -----------------------------Delete---------------------------------
@app.route('/delete_job/<job_id>')
def delete_job(job_id):
    mongo.db.jobs.remove({'_id': ObjectId(job_id)})
    return redirect(url_for('get_jobs'))


# -----------------------------Update---------------------------------
@app.route('/insert_job', methods=["POST"])
def insert_job():
    job_doc = {'job_name': request.form.get('job_name')}
    mongo.db.jobs.insert_one(job_doc)
    return redirect(url_for('get_jobs'))


# -------------------------------Create--------------------------------
@app.route('/add_job')
def add_job():
    return render_template('addjob.html')


# --------------------------------Read---------------------------------
@app.route('/get_type')
def get_type():
    return render_template('type.html', type=mongo.db.type.find())


# ------------------------------Update----------------------------------"""
@app.route('/edit_type/<type_id>')
def edit_type(type_id):
    return render_template('edittype.html',
                           type=mongo.db.type.find_one(
                            {'_id': ObjectId(type_id)}))


@app.route('/update_type/<type_id>', methods=["POST"])
def update_type(type_id):
    mongo.db.type.update({'_id': ObjectId(type_id)},
                         {'type_patient': request.form.get('type_patient')})
    return redirect(url_for('get_type'))


# ------------------------------Delete----------------------------------
@app.route('/delete_type/<type_id>')
def delete_type(type_id):
    mongo.db.type.remove({'_id': ObjectId(type_id)})
    return redirect(url_for('get_type'))


# ------------------------------Create----------------------------------
@app.route('/insert_type', methods=["POST"])
def insert_type():
    type_doc = {'type_patient': request.form.get('type_patient')}
    mongo.db.type.insert_one(type_doc)
    return redirect(url_for('get_type'))


@app.route('/add_type')
def add_type():
    return render_template('addtype.html')


# ---------------------------------Application--------------------------
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
