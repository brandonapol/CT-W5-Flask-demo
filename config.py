import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    '''
        Set config variables for the flask app
        Using Environment variables where available.
        Otherwise create the config variable if not done already
    '''

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ryan will never acquire access to my CSS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_NOTIFICAITONS = False