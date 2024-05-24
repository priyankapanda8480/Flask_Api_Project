
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/apiproject'
    SQLALCHEMY_TRACK_MODIFICATIONS = False