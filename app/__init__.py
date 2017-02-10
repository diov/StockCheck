from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap

csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_pyfile('config.py')
csrf.init_app(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
