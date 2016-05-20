from app import db, app
from flask.ext.login import LoginManager, UserMixin

lm = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
