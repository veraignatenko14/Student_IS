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
    form.subject.choices = [(subject.id, subject.name) for subject in Subjects.query.order_by(Subjects.name).all()]  # SELECT * FROM subjects ORDER BY name
    students = Students.query.all()  # достаю всех студентов из БД
    if form.validate_on_submit():
        student = Students(
            name=form.name.data,
            birth_date=form.birth_date.data,
            mark=form.mark.data,
            subject_id=form.subject.data,  # я достаю из тега option значение, которое хранится в атрибуте value (id предмета из базы даных)
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


@app.route('/update-student/<int:id>', methods=['GET', 'POST'])  # mysite.com/update/4 <- мы обвноялем конкретный элемент из базы данных по id
def update_student(id):
    """
    Function update the student information by id.
    :param id: student id from database
    :return: html template add_student page
    """
    students = Students.query.get_or_404(id)  # если id студента не будет найден в БД, вылетит ошибка 404
    form = StudentForm()
    form.subject.choices = [(subject.id, subject.name) for subject in Subjects.query.order_by(Subjects.name).all()]
    if form.validate_on_submit():  # когда форма отправляется
        students.name = form.name.data  # изменить старое имя студента на значение из поля name формы
        students.birth_date = form.birth_date.data
        students.mark = form.mark.data
        students.subject_id = form.subject.data
        students.status = form.status.data
        try:
            db.session.commit()  # обновляю данные в базе
        except:
            return 'There was a problem updating data.'
        return redirect(url_for('add_student'))
    else:
        return render_template('update-student.html', form=form, student=students)


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Students.query.get_or_404(id)  # нахожу id студента в базе
    try:
        db.session.delete(student)  # удаляю студента из БД
        db.session.commit()
        return redirect(url_for('add_student'))
    except:
        return 'There was a problem deleting student'


@app.route('/delete-subj/<int:id>')
def delete_subject(id):
    subject = Subjects.query.get_or_404(id)  # нахожу id студента в базе
    try:
        db.session.delete(subject)  # удаляю студента из БД
        db.session.commit()
        return redirect(url_for('add_subject'))
    except:
        return 'There was a problem deleting student'


@app.errorhandler(404)  # обработчик ошибки 404
def error_404(error):
    return render_template('404.html'), 404
