from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True, static_url_path='')

app.config.from_object('config')

db = SQLAlchemy(app)

from app import routes
