from flask import Flask, render_template
from config import Config
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# This was not explained in class
from models import db as root_db

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)
# this also was not explained in class
root_db.init_app(app)
# I assume this has to do with the 'Flask Migrate -m "msg"' command in terminal as I suspect the init_app method was on line 17
migrate = Migrate(app, root_db)

import models