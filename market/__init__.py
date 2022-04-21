#import Flask(download flask by [pip install flask] in cmd)
import bcrypt
from flask import Flask , render_template
#import SQLalchemy from flask_sqlalchemy[pip install flask_sqlalchemy] SQLalchemy is ORM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

#for hassing password
from flask_bcrypt import Bcrypt

#pip install flask_login
from flask_login import LoginManager

#pip install flask-mail
from flask_mail import Mail


#The variable __name__ is passed as first argument when creating an instance of the Flask object (a Python Flask application). In this case __name__ represents the name of the application package and it’s used by Flask to identify resources like templates, static assets and the instance folder.
app = Flask(__name__)

#create database in locala App
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Market_data_table.db"

#os.urandom(12).hex()
app.config['SECRET_KEY'] = '87639f81ab8fb2400290187b'
db = SQLAlchemy(app)

#hssing
bcrypt = Bcrypt(app)

#login_manager
login_manager = LoginManager(app)

login_manager.login_view = "login_page"


mail = Mail(app)


from market import models, routes 








