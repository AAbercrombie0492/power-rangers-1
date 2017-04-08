import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Set up a local sqlite database
SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False')
SQLALCHEMY_TRACK_MODIFICATIONS=False
