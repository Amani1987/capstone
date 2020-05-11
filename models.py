from flask import Flask
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import json
import os


#DATABASE_URI = os.getenv('DATABASE_URI')
DATABASE_URL = "postgres://peqqpvjpwjowch:b124205ee5f72ec25c706e1434f424b55079faed7436821ca9df198e199d0215@ec2-52-202-22-140.compute-1.amazonaws.com:5432/daerr06qc2hf52"
#
db = SQLAlchemy()

def set_up_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


# Actor


class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    movies = db.relationship('Movies',
                             lazy='dynamic', backref=db.backref('actors'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Movie


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    release_date = db.Column(db.DateTime())

    def __init__(self, title, release):
        self.title = title
        self.release = release
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
