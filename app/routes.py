from flask import Blueprint, render_template
from flask import request, jsonify, session, url_for, redirect
from .models import db, Profesores, Cuentas, Perfiles
from sqlalchemy import or_
import hashlib
import os

main = Blueprint('main',__name__)


@main.route('/')
def index():
    if 'usuario' in session:
        return render_template('index.html', usuario=session['usuario'])
    else:
        return render_template('index.html')

@main.route('/registro')
def formulario():
    return render_template('registro.html')

@main.route('/ingreso')
def ingresar():
     return render_template('iniciar.html')

@main.route('/<nombre>', methods=['GET'])
def perfil(nombre):
    if 'usuario' in session:
        nombre_id = Profesores.query.filter_by(nombre=nombre).first()
        opiniones = Perfiles.query.filter_by(nombre_id=nombre_id.id).all()
        den = len(opiniones)
        if den == 0:
            den = 1
        num1=0
        num2=0
        for opinion in opiniones:
            num1 += opinion.calificacion
            num2 += opinion.dificultad
        prom_calif = round(num1/den, 2)
        prom_dif = round(num2/den, 2)
        return render_template('perfil.html', usuario=session['usuario'], 
                               nombre=nombre, nombre_id=nombre_id, opiniones=opiniones, prom_calif=prom_calif, prom_dif=prom_dif)
    else:
        return render_template('iniciar.html')

@main.route('/registro_profesores')
def registro_profesores():
    if 'usuario' in session:
        return render_template('new_profe.html', usuario=session['usuario'])
    else:
        return render_template('new_profe.html')

@main.route('/<nombre>/nuevo_comentario', methods=['GET'])
def nuevo_comentario(nombre):
    if 'usuario' in session:
        return render_template('comentario.html', usuario=session['usuario'], nombre=nombre)
    else:
        return render_template('iniciar.html')

@main.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    return redirect(url_for('main.index'))

@main.route('/teacher_form', methods=['POST'])
def teacher_form():
    nombre=request.form.get('nombre')
    facultad=request.form.get('facultad')
    materias=request.form.get('materias')
    nuevo_profe=Profesores(nombre=nombre,
                           facultad=facultad,
                           materias=materias)
    db.session.add(nuevo_profe)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/coment_form', methods=['POST'])
def coment_form():
    nombre=request.form.get('nombre')
    usuario=request.form.get('usuario')
    calificacion=request.form.get('calificacion')
    dificultad=request.form.get('dificultad')
    comentario=request.form.get('comentario')
    nombre_id = Profesores.query.filter_by(nombre=nombre).first()
    usuario_id = Cuentas.query.filter_by(usuario=usuario).first()
    nuevo_post=Perfiles(nombre_id=nombre_id.id,
                        usuario=usuario_id.usuario,
                        calificacion=calificacion,
                        dificultad=dificultad,
                        comentario=comentario)
    db.session.add(nuevo_post)
    db.session.commit()
    return redirect(url_for('main.perfil', nombre=nombre))

@main.route('/check_form', methods=['POST'])
def check_form():
    usuario=request.form.get('usuario')
    password=request.form.get('password')
    e_usuario = Cuentas.query.filter_by(usuario=usuario).first()
    if not e_usuario:
        return jsonify({
                'status': 'error',
                'message': 'El usuario o contraseña son incorrectos.'
            }), 400
    salted_password = password.encode() + e_usuario.salt
    password_hash = hashlib.pbkdf2_hmac('sha256', salted_password, e_usuario.salt, 100000)
    if password_hash != e_usuario.password_hash:
        return jsonify({
                'status': 'error',
                'message': 'El usuario o contraseña son incorrectos.'
            }), 400
    else:
        session['usuario'] = usuario
        return redirect(url_for('main.index'))

@main.route('/submit_form', methods=['POST'])
def submit_form():
    usuario=request.form.get('usuario')
    email=request.form.get('email')
    password=request.form.get('password')
    salt = os.urandom(16)
    salted_password = password.encode() + salt
    password_hash = hashlib.pbkdf2_hmac('sha256', salted_password, salt, 100000)
    e_usuario = Cuentas.query.filter_by(usuario=usuario).first()
    if e_usuario:
            return jsonify({
                'status': 'error',
                'message': 'El usuario ya está en uso. Por favor, elige otro nombre de usuario.'
            }), 400
    nueva_cuenta=Cuentas(usuario=usuario,
                          email=email,
                          password_hash=password_hash,
                          salt=salt)
    db.session.add(nueva_cuenta)
    db.session.commit()

    session['usuario'] = usuario
    return redirect(url_for('main.index'))

@main.route('/profesores', methods=['POST'])
def ver_profesores():
    if 'usuario' in session:
        profesor = request.form.get('nombre_profesor')
        e_profesor=Profesores.query.filter(or_(Profesores.nombre.ilike(f'%{profesor}%'), Profesores.nombre.ilike(f'{profesor}%'))).all()
        if e_profesor:
            return render_template('profes.html', usuario=session['usuario'], e_profesor=e_profesor)
        else:
            return render_template('profes.html', usuario=session['usuario'], e_profesor=None)
    else:
        return render_template('iniciar.html')
