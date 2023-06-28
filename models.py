from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from enum import unique
db = SQLAlchemy(app)

class Preceptor(db.Model):
    __tablename__='preceptor'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(80),nullable=False)
    apellido=db.Column(db.String(80), nullable=False)
    correo=db.Column(db.String(120), unique=True, nullable=False)
    clave=db.Column(db.String(120),nullable=False)
    curso=db.relationship('Curso', backref='preceptor', cascade='all, delete-orphan')

class Padre(db.Model):
    __tablename__='padre'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(80), nullable=False)
    apellido=db.Column(db.String(80), nullable=False)
    correo=db.Column(db.String(120), unique=True, nullable=False)
    clave=db.Column(db.String(120), nullable=False)

class Estudiante(db.Model):
    __tablename__='estudiante'
    id=db.Column(db.Integer,primary_key=True)
    dni=db.Column(db.String(20))
    nombre=db.Column(db.Text)
    apellido=db.Column(db.Text)
    idcurso=db.Column(db.Integer, db.ForeignKey('curso.id'))
    idpadre=db.Column(db.Integer, db.ForeignKey('padre.id'))

class Curso(db.Model):
    __tablename__='curso'
    id=db.Column(db.Integer,primary_key=True)
    anio=db.Column(db.String(80))
    division=db.Column(db.String(80))
    idpreceptor=db.Column(db.Integer, db.ForeignKey('preceptor.id'))

class Asistencia(db.Model):
    __tablename__='asistencia'
    id=db.Column(db.Integer,primary_key=True)
    fecha=db.Column(db.DateTime)
    codigoclase=db.Column(db.Integer)
    asistio=db.Column(db.Text)
    justificacion=db.Column(db.String(100))
    idestudiante=db.Column(db.Integer, db.ForeignKey('estudiante.id'))