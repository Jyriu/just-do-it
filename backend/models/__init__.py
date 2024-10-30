from flask_sqlalchemy import SQLAlchemy
from extensions import db
from .user import User
from .post import Post


__all__ = ['User', 'Post']