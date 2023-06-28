from datetime import datetime
from flask import Flask
from flask import request, render_template,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
app=Flask(__name__)#nombre del modulo actual de python, indica todo lo q pertenece a su app

app.config.from_pyfile('config.py')
from models import db
from models import Preceptor, Padre, Estudiante, Curso, Asistencia

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/iniciar_sesion', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if not request.form['correo'] or not request.form['contraseña'] or not request.form['cargo']:
            return render_template('error.html', error='Por favor ingrese todos los datos requeridos.')
        else:
            if request.form['cargo']=='Preceptor':
                c=request.form['correo']
                unPreceptor=Preceptor.query.filter_by(correo=c).first()
                claveP=hashlib.md5(bytes(request.form['contraseña'],encoding='utf-8'))
                verificacion=unPreceptor.clave==claveP.hexdigest()
                if unPreceptor is None:
                    return render_template('error.html',error='El correo no está registrado.')
                else:
                    if verificacion:
                        session['preceptorId']=unPreceptor.id
                        return render_template('opcion.html')
                    else:
                        return render_template('error.html', error='Los datos ingresados no son correctos')
            else:
                return render_template('error.html', error='Se debe ingresar una opcion valida')
    else:
        return render_template('inicio.html')
           

@app.route('/seleccionar_opcion', methods=['GET','POST'])
def select_opcion():
    if request.method == 'POST':
        op=request.form['opS']
        if op=='1' or op=='2':
            cursos = Curso.query.filter_by(idpreceptor = session.get('preceptorId')).all()
            return render_template('opcion.html', op=op, cursos=cursos)
        return render_template('opcion.html', op=op)    


@app.route('/seleccionar_curso', methods=['GET','POST'])
def select_curso():
    if request.method == 'POST':
        op=request.form['opS']
        cursos = Curso.query.filter_by(idpreceptor = session.get('preceptorId')).all()
        if op=='1':
            curso = request.form['curso']
            alumnos = Estudiante.query.filter_by(idcurso = curso).all()
            return render_template('opcion1.html', opS=op, op=op, alumnos=alumnos, cursos=cursos)
        if op=='2':
            resultado = []
            curso = request.form['curso']
            alumnos = Estudiante.query.filter_by(idcurso = curso).order_by(Estudiante.nombre).all()
            for estudiante in alumnos:
                presentes_aula = Asistencia.query.filter_by(codigoclase=1, asistio='s', idestudiante=estudiante.id).count()
                presentes_educacion_fisica  = Asistencia.query.filter_by(codigoclase=2, asistio='s', idestudiante=estudiante.id).count()

                ausentes_educacion_fisica_justificadas = Asistencia.query.filter(
                                            Asistencia.codigoclase == 2,
                                            Asistencia.asistio == 'n',
                                            Asistencia.idestudiante == estudiante.id,
                                            Asistencia.justificacion != ''
                                            ).count()
                ausentes_aula_justificadas = Asistencia.query.filter(
                                            Asistencia.codigoclase == 1,
                                            Asistencia.asistio == 'n',
                                            Asistencia.idestudiante == estudiante.id,
                                            Asistencia.justificacion != ''
                                            ).count()
                
                ausentes_aula_injustificadas = Asistencia.query.filter(
                                            Asistencia.codigoclase == 1,
                                            Asistencia.asistio == 'n',
                                            Asistencia.idestudiante == estudiante.id,
                                            Asistencia.justificacion == ''
                                            ).count()
                ausentes_educacion_fisica_ijustificadas = Asistencia.query.filter(
                                            Asistencia.codigoclase == 2,
                                            Asistencia.asistio == 'n',
                                            Asistencia.idestudiante == estudiante.id,
                                            Asistencia.justificacion == ''
                                            ).count()
            
                total_inasistencias = (Asistencia.query.filter_by(codigoclase=1, asistio='n', idestudiante=estudiante.id).count(
                ) * 1) + (Asistencia.query.filter_by(codigoclase=2, asistio='n', idestudiante=estudiante.id).count() * 0.5)

                resultado.append({
                    'nombre': estudiante.nombre,
                    'apellido': estudiante.apellido,
                    'id': estudiante.id,
                    'presentes_aula': presentes_aula,
                    'presentes_educacion_fisica': presentes_educacion_fisica,
                    'ausentes_educacion_fisica_justificadas': ausentes_educacion_fisica_justificadas,
                    'ausentes_aula_justificadas': ausentes_aula_justificadas,
                    'ausentes_aula_injustificadas': ausentes_aula_injustificadas,
                    'ausentes_educacion_fisica_ijustificadas': ausentes_educacion_fisica_ijustificadas,
                    'total_inasistencias': total_inasistencias,
                })
            return render_template('opcion2.html', opS=op, op=op, cursos=cursos, resultado=resultado)
        return render_template('opcion.html', op=op)


@app.route('/guardar_asistencia', methods=['GET','POST'])
def guardar_asistencia():
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        ids = request.form.getlist('ids')
        justificaciones = request.form.getlist('justificaciones')
        clases = request.form.getlist('clases')
        asistencias = request.form.getlist('asistencias')
        for i in range(len(ids)):
            id = ids[i]
            justificacion = justificaciones[i]
            clase = clases[i]
            asistencia = asistencias[i]
            nueva_asistencia = Asistencia(fecha=fecha, codigoclase=clase, asistio=asistencia, justificacion=justificacion, idestudiante=id)
            db.session.add(nueva_asistencia)
            db.session.commit()
        return render_template('opcion.html')
@app.route("/volver_pricipal",  methods=['GET','POST'])
def volver():
    if request.method == 'POST':
        return render_template("inicio.html")
if __name__=='__main__':
    app.run(debug=True)