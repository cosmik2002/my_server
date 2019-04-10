from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
engine = create_engine('firebird://SYSDBA:123@serv2:3050/e:\\supermag.gdb?charset=utf8')
meta = MetaData()
link_types = Table('link_types', meta, autoload=True, autoload_with=engine)
print(repr(link_types))
Session = sessionmaker(bind=engine)
session = Session()
res = session.query(link_types).all()
print(repr(res))
