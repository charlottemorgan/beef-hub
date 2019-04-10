from marshmallow import fields
from app import db, ma
from .base import BaseModel, BaseSchema
# pylint: disable=W0611
from .category import Category
from .user import User
from .comment import Comment

likes = db.Table(
    'likes',
    db.Column('beef_id', db.Integer, db.ForeignKey('beefs.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

categories_beefs = db.Table('categories_beefs',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
    db.Column('beef_id', db.Integer, db.ForeignKey('beefs.id'), primary_key=True)
)

followers_beefs = db.Table(
  'followers_beefs',
  db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('beef_id', db.Integer, db.ForeignKey('beefs.id'))
)


class Beef(db.Model, BaseModel):

    __tablename__ = 'beefs'

    beefer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beefer = db.relationship('User', foreign_keys=[beefer_id],backref='created_beefs')
    beefee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beefee = db.relationship('User', foreign_keys=[beefee_id], backref='beefs_against')
    reason = db.Column(db.String, nullable=False)
    still_beefing = db.Column(db.Boolean, nullable=False, default=True)
    categories = db.relationship('Category', secondary=categories_beefs, backref='beefs')
    liked_by = db.relationship('User', secondary=likes, backref='likes')
    followed_by = db.relationship('User', secondary=followers_beefs, backref='beefs_followed')

class BeefSchema(ma.ModelSchema, BaseSchema):

    beefer = fields.Nested('UserSchema', only=('id', 'username'))
    beefee = fields.Nested('UserSchema', only=('id', 'username'))
    comments = fields.Nested('CommentSchema', many=True, only=('content', 'id'))
    categories = fields.Nested('CategorySchema', many=True, only=('name', 'id'))
    liked_by = fields.Nested('UserSchema', many=True, only=('id', 'username'))
    followed_by = fields.Nested('UserSchema', many=True, only=('id', 'username'))

    class Meta:
        model = Beef
