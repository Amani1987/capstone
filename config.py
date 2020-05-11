import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Database connection string
DATABASE_URL = "postgres://peqqpvjpwjowch:b124205ee5f72ec25c706e1434f424b55079faed7436821ca9df198e199d0215@ec2-52-202-22-140.compute-1.amazonaws.com:5432/daerr06qc2hf52"
#Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
