from . import db
from sqlalchemy import ForeignKey

class Cuentas(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    usuario=db.Column(db.String(50), unique=True)
    email=db.Column(db.String(100))
    password_hash=db.Column(db.BLOB)
    salt=db.Column(db.BLOB)

class Profesores(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(100))
    facultad=db.Column(db.String(100))
    materias=db.Column(db.String(100))

class Perfiles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre_id=db.Column(db.Integer, ForeignKey('profesores.id'))
    usuario=db.Column(db.String(50), ForeignKey('cuentas.usuario'))
    calificacion=db.Column(db.Integer)
    dificultad=db.Column(db.Integer)
    comentario=db.Column(db.String(300))
