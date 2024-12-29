import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False, unique=True)
    follower = relationship('Follower', back_populates='user_from')
    followed = relationship('Follower', back_populates='user_to')
    post_user = relationship('Post', back_populates='user')
    comment_user = relationship('Comment', back_populates='author')
    #author = relationship(User, back_populates='comment_user')
    #user = relationship(User, back_populates='post')
    #user_from = relationship(User)

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_from = relationship(User, back_populates='follower')
    user_to_id = Column(Integer, ForeignKey('user.id'))
    user_to = relationship(User, back_populates='followed')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, back_populates='post_user')
    comment_post = relationship('Comment', back_populates='post')
    media_post = relationship('Media', back_populates='post')
    #post = relationship(Post, back_populates='comment_post')
    #post = relationship(Post, back_populates='media_post')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship(User, back_populates='comment_user')
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship(Post, back_populates='comment_post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'audio', name='media_type_enum'), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship(Post, back_populates='media_post')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
