import sys
sys.path.insert(0, r'E:\Nicholas\python\my_server')
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///srv1.sqb',
    # SQLALCHEMY_DATABASE_URI='firebird://SYSDBA:123@serv2:3050/e:\\supermag.gdb?charset=utf8',
    SQLALCHEMY_BINDS = {
        'fakturace':   'firebird://SYSDBA:masterkey@localhost:3051/c:\\datawalsoft\\datawalsoft3.fdb?charset=utf8',
        'supermag':    'firebird://SYSDBA:123@serv2:3050/e:\\supermag.gdb?charset=utf8',
        'main':'sqlite:///srv.sqb'
   },
   SQLALCHEMY_TRACK_MODIFICATIONS=False

    )
db = SQLAlchemy(app)
db.reflect(app=app)
class User(db.Model):
    pass
#   __bind_key__ = 'main'
   #__table_args__={
   #    'autoload':True,
   #    'autoload_with':db.engine
   #}
   #pass
#class test(db.Model):
#   __bind_key__ = 'main'
class objects(db.Model):
    __bind_key__='supermag'


class operations(db.Model):
    __bind_key__='supermag'
    __table_args__={
        "autoload":True,
        'autoload_with':db.get_engine(bind='supermag'),
        'extend_existing': True
    }
    client1 = db.Column(db.Integer,db.ForeignKey("clients.id"))

class clients(db.Model):
    __bind_key__='supermag'


#clients.operations = db.relationship("operations",backref="client1obj",primaryjoin=(operations.client1==clients.id))
operations.client1obj = db.relationship("clients",primaryjoin=(operations.client1==clients.id))

class link_types_v(db.Model):
    # pass
    __bind_key__='supermag'
    id = db.Column(db.Integer,primary_key=True)
    # __tablename__ = 'LINK_TYPES'
    __table_args__ = {
        'autoload':True,
        'autoload_with':db.get_engine(bind='supermag')
    }

class knihafaktur(db.Model):
     __bind_key__ = 'fakturace'
     #__tablename__ = 'knihafaktur'
     #__table_args__ = {
     #   'autoload':True,
     #   'autoload_with':db.get_engine(bind='fakturace')
     #}

#print(User.query.all()[1].email)

print(User.__table__.columns)
print(link_types_v.__table__.columns)
print(objects.__table__.columns)
print(operations.query.first().client1obj.__dict__)

print(knihafaktur.__table__.columns)