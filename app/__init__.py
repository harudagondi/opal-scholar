from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object('config')
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': config.FB_ID,
        'secret': config.FB_SECRET
    }
}
db = SQLAlchemy(app)

from app import views, models
