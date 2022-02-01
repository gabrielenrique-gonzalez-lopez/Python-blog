from flask import Flask
from . import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '4a627695fb3c729e7a4014572ab33d52'
app.config['DATABASE'] = 'sqlite:///site.db'

db.init_app(app)
from . import routes