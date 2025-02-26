from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    student = db.relationship('Students', backref='subjects', lazy=True)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False, default=datetime.now())
    mark = db.Column(db.Float, nullable=False, default=3.2)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    status = db.Column(db.String(10), nullable=False, default='Paid')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    subject_id = db.relationship('Subjects', backref='teachers', lazy=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.now())
    time = db.Column(db.Time, default=datetime.now())

    teacher_id = db.relationship('Teachers', backref='lessons', lazy=True)
    subj_id = db.relationship('Subjects', backref='lessons', lazy=True)



