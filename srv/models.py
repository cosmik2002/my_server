import base64
import os
from srv import db
from datetime import datetime,timedelta
from flask_login import UserMixin
from srv import login
from flask import flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil.tz import tzutc, tzlocal

class ToDictInterfaceMixin(object):
    """serialize table record to dict"""
    def to_dict(self):
        """serialize table record to dict"""
        d={}
        for col in self.__table__.columns:
          if 'visible' not in col.info or col.info['visible'] is not False:
              if isinstance(getattr(self, col.key),datetime):
                  d[col.key] = getattr(self, col.key).replace(tzinfo=tzutc()).astimezone(tzlocal()).strftime('%d.%m.%Y %H:%M')
              else:
                  d[col.key]=getattr(self, col.key)
        return d


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page,per_page, False)
        data = {
         'items':[item.to_dict() for item in resources.items],
         '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': resources.pages,
            'total_items': resources.total
          },
          '__links':{
             'self': url_for(endpoint,page=page,per_page = per_page,**kwargs),
             'next': url_for(endpoint,page=page + 1,per_page = per_page,**kwargs) if resources.has_next else None,
             'prev': url_for(endpoint,page=page - 1,per_page = per_page,**kwargs) if resources.has_prev else None,
          }
        }
        return data




# class test(db.Model):
#     pass
    #INDEXZAZNAMU = db.Column(db.Integer,primary_key=True)
    #cislofa = db.Column(db.Integer,primary_key=True)

class knihafaktur(db.Model):
    __bind_key__ = 'fakturace'
    numodberatel = db.Column(db.Integer, db.ForeignKey("adresy.indexzaznamu"))
#    __tablename__ = 'knihafaktur'
    __table_args__ = {
        'extend_existing': True
#        'autoload':True,
#        'autoload_with':db.get_engine(bind='fakturace')
    }
    #INDEXZAZNAMU = db.Column(db.Integer,primary_key=True)
    #cislofa = db.Column(db.Integer,primary_key=True)


class knihafakturpolozky(db.Model):
    __bind_key__ = 'fakturace'


class adresy(db.Model):
    __bind_key__ = 'fakturace'


class odberatele_311(db.Model):
    __bind_key__ = 'fakturace'

#operations.client1obj = db.relationship("clients",primaryjoin=(operations.client1==clients.id))
knihafaktur.adresy = db.relationship("adresy", primaryjoin=(knihafaktur.numodberatel == adresy.indexzaznamu))

class Log(ToDictInterfaceMixin, db.Model):
    date_time = db.Column(db.DateTime,primary_key=True,default=datetime.utcnow)
    log_type = db.Column(db.String(50),index=True)
    message = db.Column(db.String(512))


class Climate(db.Model):
    date_time = db.Column(db.DateTime,primary_key=True,default=datetime.utcnow)       
    type = db.Column(db.String(50),index=True)
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)


class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)       
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32),index = True, unique = True)
    token_expiration = db.Column(db.DateTime)

    def get_token(self,expires_in=3600):
       now = datetime.utcnow()
       if self.token and self.token_expiration > now + timedelta(seconds=60):
          return self.token
       self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
       self.token_expiration = now + timedelta(seconds=expires_in)
       db.session.add(self)
       return self.token

    def revoke_token(self):
       self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
       user = User.query.filter_by(token=token).first()
       if user is None or user.token_expiration < datetime.utcnow():
          return None
       return user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        #self.password_hash = password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        #return self.password_hash == password;
    #def __repr__(self):
    #    return '<User {}>'.format(self.username) 

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username','email','about_me']:
           if field in data:
              setattr(self,field,data[field])
        if new_user and 'password' in data:
           self.set_password(data['password'])
         

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

