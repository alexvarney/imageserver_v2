from flask import Flask
from flask_bootstrap import Bootstrap
from imageserver.main.controllers import main
from imageserver.admin.controllers import admin


app = Flask(__name__)
Bootstrap(app)

app.config.from_pyfile('config.py')
app.register_blueprint(main, url_prefix='')
app.register_blueprint(admin, url_prefix='/admin')
