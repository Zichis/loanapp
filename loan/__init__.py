from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'efcbbc20c1134fd8ef5410ac745c2c6261fe9836'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_APP_NAME'] = 'PBank'
app.config['USER_ENABLE_USERNAME'] = False

db = SQLAlchemy(app)

from loan import routes