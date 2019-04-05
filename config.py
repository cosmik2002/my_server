import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1you-will-never-guess1'
#    SERVER_NAME = os.environ.get('SERVER_NAME') 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir,'srv.sqb')
    SQLALCHEMY_BINDS = {
        'fakturace':    'firebird://SYSDBA:masterkey@localhost:3051/c:\\datawalsoft\\datawalsoft3.fdb?charset=utf8'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['nicholas-r@mail.ru']
    OPERATIONS_PER_PAGE = 30