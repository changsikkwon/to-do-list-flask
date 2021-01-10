from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

from config import DB_URL

database = create_engine(DB_URL, encoding='utf-8')
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=database))
Base = declarative_base()
Base.Query = Session.query_property()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    account = Column(String)
    password = Column(String)
    is_master = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag = Column(String)


class ToDoList(Base):
    __tablename__ = 'to_do_list'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    is_completed = Column(Boolean)
    target_date = Column(DateTime)
    complete_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('users', cascade='delete,all'))
    tag_id = Column(Integer, ForeignKey('tag.id'), default=1)