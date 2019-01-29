from loan import db
from flask_user import UserMixin

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  active = db.Column(db.Boolean(), nullable=False, default=True)
  profile = db.relationship('Profile', backref='user', uselist=False)
  accounts = db.relationship('Account', backref='owner', lazy=True)
  loan_profiles = db.relationship('LoanProfile', backref='loanee', lazy=True)
  roles = db.relationship('Role', secondary='user_roles')

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
  __tablename__ = 'user_roles'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

class Profile(db.Model):
  __tablename__ = 'profiles'
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(50))
  middlename = db.Column(db.String(50))
  lastname = db.Column(db.String(50))
  gender = db.Column(db.String(1))
  nationality = db.Column(db.String(100))
  profile_image = db.Column(
      db.String(20), nullable=False, default='default.jpg')
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

class Account(db.Model):
  __tablename__ = 'accounts'
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.String(20), unique=True)
  balance = db.Column(db.Integer)
  outstanding = db.Column(db.Integer, default='0.00')
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


class LoanProfile(db.Model):
  __tablename__ = 'loan_profiles'
  id = db.Column(db.Integer, primary_key=True)
  annual_income = db.Column(db.String(50))
  loan_amount = db.Column(db.String(50))
  purpose_of_loan = db.Column(db.String(50))
  home_ownership = db.Column(db.String(50))
  term = db.Column(db.String(50))
  time_of_employment = db.Column(db.String(5))
  borrower_deliquency = db.Column(db.String(5))
  dti = db.Column(db.String(50))
  length_of_employment = db.Column(db.String(50))
  percentage_available_credit = db.Column(db.String(50))
  total_late_fees = db.Column(db.String(50))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)