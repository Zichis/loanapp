from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

class AddAdminForm(FlaskForm):
  firstname = StringField('First name', validators=[DataRequired()])
  middlename = StringField('Middle name', validators=[DataRequired()])
  lastname = StringField('Last name', validators=[DataRequired()])
  gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
  nationality = SelectField('Nationality', choices=[('Nigerian', 'Nigerian'), ('Ghanaian', 'Ghanaian')])
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

class AddUserForm(FlaskForm):
  firstname = StringField('First name', validators=[DataRequired()])
  middlename = StringField('Middle name', validators=[DataRequired()])
  lastname = StringField('Last name', validators=[DataRequired()])
  gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
  nationality = SelectField('Nationality', choices=[('Nigerian', 'Nigerian'), ('Ghanaian', 'Ghanaian')])
  account_number = StringField('Account number', validators=[DataRequired()])
  balance = StringField('Deposit', validators=[DataRequired()])
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

options = [
  [
    ('1', 'RENT'), ('2', 'OWN'), ('3', 'MORTGAGE'), ('4', 'OTHER')
  ],
  [
    ('36', '36 months'), ('60', '60 months')
  ],
  [
    ('1', 'Credit card'), ('2', 'Car'), ('3', 'Small business'), ('4', 'Other'), ('5', 'Wedding'),
    ('6', 'Debt consolidation'), ('7', 'Home improvement'), ('8', 'Major purchase'), ('9', 'Medical'),
    ('10', 'Moving'), ('11', 'Vacation'), ('12', 'House')
  ]
]

class LoanStatusForm(FlaskForm):
  annual_income = StringField('Annual income', validators=[DataRequired()])
  loan_amount = StringField('Loan amount', validators=[DataRequired()])
  purpose_of_loan = SelectField('Purpose of loan', choices = options[2])
  home_ownership = SelectField('Home ownership', choices = options[0])
  term = SelectField('Term', choices = options[1])
  short_emp = SelectField('Time of employment', choices=[('0', 'Less than a year'), ('1', 'A year and above')])
  last_delinq_none = SelectField('Borrower deliquency', choices=[('0', 'No'), ('1', 'Yes')])
  dti = StringField('Debt To Income Ratio', validators=[DataRequired()])
  emp_length_num = StringField('Length of employment', validators=[DataRequired()])
  revol_util = StringField('Percentage available credit', validators=[DataRequired()])
  total_rec_late_fee = StringField('Total late fees received', validators=[DataRequired()])