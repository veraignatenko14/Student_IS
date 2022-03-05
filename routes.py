from flask import render_template, redirect, url_for
from app import app, db
from forms import StudentForm, SubjectForm
from models import Subjects, Students


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    students = Students.query.all()  # достаю всех студентов из БД
    if form.validate_on_submit():
        student = Students(
            name=form.name.data,
            birth_date=form.birth_date.data,
            mark=form.mark.data,
            status=form.status.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('add_student'))

    return render_template('add_students.html', form=form, items=students)


@app.route('/add-subject', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()
    subjects = Subjects.query.order_by(Subjects.name).all()  # SELECT * FROM subjects ORDER BY name
    if form.validate_on_submit():
        subj = Subjects(
            name=form.name.data
        )
        db.session.add(subj)
        db.session.commit()
        return redirect(url_for('add_subject'))
    return render_template('add_subject.html', form=form, items=subjects)
