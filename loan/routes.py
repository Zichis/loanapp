from loan import app, db
from flask import render_template, flash, redirect, url_for
from loan.models import User, Profile, Account, Role, LoanProfile
from flask_user import login_required, UserManager, roles_required, current_user
from flask_user.db_manager import DBManager
from loan.forms import AddUserForm, AddAdminForm, LoanStatusForm
from loan.randomforest import RandomForestAlgorithm
from loan.functions import modify_home_ownership, modify_purpose, modify_term, modify_time_of_employment

user_manager = UserManager(app, db, User)
db_manager = DBManager(app, db, User, UserEmailClass=None, UserInvitationClass=None, RoleClass=Role)

db.create_all()

if len(User.query.all()) < 1:
  user = User(
    username = 'PB1508',
    email = 'pahueze@gmail.com',
    password = user_manager.hash_password('asdfghjkl'),
    active = True
  )

  user.roles.append(Role(name='Admin'))

  db.session.add(user)
  db.session.commit()

  profile = Profile(
    firstname = 'Peter',
    middlename = 'Mike',
    lastname = 'Ahueze',
    gender = 'male',
    nationality = 'Nigerian',
    user_id = user.id
  )

  db.session.add(profile)
  db.session.commit()

@app.route('/')
def home():
  if current_user.is_authenticated:
    profile = Profile.query.filter_by(id = current_user.id).all()
    user = User.query.filter_by(id = current_user.id).all()
    userRole = user[0].roles[0].name.lower()
  else:
    profile = ['Error']
    userRole = 'Error'
  return render_template('index.html', profile=profile[0], userRole=userRole)

@app.route('/contact')
def contact():
  if current_user.is_authenticated:
    profile = Profile.query.filter_by(id = current_user.id).all()
    user = User.query.filter_by(id = current_user.id).all()
    userRole = user[0].roles[0].name.lower()
  else:
    profile = ['Error']
    userRole = 'Error'
  return render_template('contact.html', profile=profile[0], userRole=userRole)

@app.route('/about')
def about():
  if current_user.is_authenticated:
    profile = Profile.query.filter_by(id = current_user.id).all()
    user = User.query.filter_by(id = current_user.id).all()
    userRole = user[0].roles[0].name.lower()
  else:
    profile = ['Error']
    userRole = 'Error'
  return render_template('about.html', profile=profile[0], userRole=userRole)

@app.route('/admin/dashboard')
@roles_required('Admin')
def admin_dashboard():
  profile = Profile.query.filter_by(id = current_user.id).all()
  customers = getAllCustomers(4)
  admins = getAllAdmins('all')
  customer_number = Account.query.count()

  accounts = Account.query.all()
  balance_sum = 0

  for account in accounts:
    balance_sum += account.balance
  
  return render_template(
    'admin_dashboard.html', 
    profile=profile[0], 
    customers=customers, 
    admins=admins, 
    customer_number=customer_number, 
    balance_sum=balance_sum)

@app.route('/admin/customers')
@roles_required('Admin')
def admin_customers():
  profile = Profile.query.filter_by(id = current_user.id).all()
  customers = getAllCustomers('all')
  return render_template('admin_customers.html', profile=profile[0], customers=customers)

@app.route('/admin/customer/<user_id>')
@roles_required('Admin')
def admin_customer_id(user_id):
  profile = Profile.query.filter_by(user_id = current_user.id).all()
  customer_profile = Profile.query.filter_by(user_id = user_id).all()
  accounts = Account.query.filter_by(user_id = user_id).all()
  loan_profiles = LoanProfile.query.filter_by(user_id = user_id).all()
  return render_template('admin_customer_single.html', profile=profile[0], customer_profile=customer_profile[0], accounts=accounts, loan_profiles=loan_profiles)

@app.route('/admin/customer_add', methods=['POST', 'GET'])
@roles_required('Admin')
def admin_customer_add():
  form = AddUserForm()
  profile = Profile.query.filter_by(user_id = current_user.id).all()

  if form.validate_on_submit():

    new_user = User(username = form.username.data, email = form.email.data, password = user_manager.hash_password(form.password.data))
    db.session.add(new_user)
    db.session.commit()

    db_manager.add_user_role(new_user, 'Customer')
    db_manager.commit()

    new_profile = Profile(
      firstname = form.firstname.data,
      middlename = form.middlename.data,
      lastname = form.lastname.data,
      gender = form.gender.data,
      nationality = form.nationality.data,
      user_id = new_user.id
    )

    db.session.add(new_profile)
    db.session.commit()

    new_account = Account(
      number = form.account_number.data,
      balance = form.balance.data,
      user_id = new_user.id
    )

    db.session.add(new_account)
    db.session.commit()

    flash('New customer added', 'success')

    return redirect(url_for('admin_customers'))
  return render_template('admin_customer_add.html', profile=profile[0], form=form)

@app.route('/admin/admins')
@roles_required('Admin')
def admin_admins():
  profile = Profile.query.filter_by(id = 1).all()
  admins = getAllAdmins('all')
  return render_template('admin_admins.html', profile=profile[0], admins=admins)

@app.route('/admin/admin_user/<user_id>')
@roles_required('Admin')
def admin_admin_user_id(user_id):
  profile = Profile.query.filter_by(user_id = current_user.id).all()
  admin_profile = Profile.query.filter_by(user_id = user_id).all()
  return render_template('admin_admin_single.html', profile=profile[0], admin_profile=admin_profile[0])

@app.route('/admin/admin_add', methods=['POST', 'GET'])
@roles_required('Admin')
def admin_admin_add():
  form = AddAdminForm()
  profile = Profile.query.filter_by(user_id = current_user.id).all()

  if form.validate_on_submit():
    new_user = User(username = form.username.data, email = form.email.data, password = user_manager.hash_password(form.password.data))
    db.session.add(new_user)
    db.session.commit()

    db_manager.add_user_role(new_user, 'Admin')
    db_manager.commit()

    new_profile = Profile(
      firstname = form.firstname.data,
      middlename = form.middlename.data,
      lastname = form.lastname.data,
      gender = form.gender.data,
      nationality = form.nationality.data,
      user_id = new_user.id
    )

    db.session.add(new_profile)
    db.session.commit()

    flash('New admin added', 'success')

    return redirect(url_for('admin_admins'))
  
  return render_template('admin_admin_add.html', form=form, profile=profile[0])

@app.route('/admin/remove_user_confirmation/<user_id>', methods=['POST', 'GET'])
@roles_required('Admin')
def admin_remove_user_confirmation(user_id):
  user_profile = Profile.query.filter_by(id = user_id).all()
  return render_template('admin_remove_user_confirmation.html', user_id=user_id, user_profile=user_profile[0])

@app.route('/admin/remove_user/<user_id>', methods=['POST', 'GET'])
@roles_required('Admin')
def admin_remove_user(user_id):
  user = User.query.filter_by(id = user_id).all()
  role = user[0].roles[0].name

  if role == 'Customer':
    user = Account.query.filter_by(user_id = user_id).all()
    db.session.delete(user[0])
    db.session.commit()

    user = Profile.query.filter_by(user_id = user_id).all()
    db.session.delete(user[0])
    db.session.commit()

    user = User.query.filter_by(id = user_id).all()
    db.session.delete(user[0])
    db.session.commit()
  elif role == 'Admin':
    user = Profile.query.filter_by(user_id = user_id).all()
    db.session.delete(user[0])
    db.session.commit()

    user = User.query.filter_by(id = user_id).all()
    db.session.delete(user[0])
    db.session.commit()

  flash("User's record has been removed!", "success")
  return redirect(url_for('admin_dashboard'))
  #return "You are about to remove user with ID of " + user_id

# Customer routes
@app.route('/customer/dashboard')
@roles_required('Customer')
def customer_dashboard():
  profile = Profile.query.filter_by(user_id = current_user.id).all()
  accounts = Account.query.filter_by(user_id = current_user.id).all()
  return render_template('customer_dashboard.html', profile=profile[0], accounts=accounts)

@app.route('/customer/profile')
@roles_required('Customer')
def customer_profile():
  profile = Profile.query.filter_by(user_id = current_user.id).all()
  accounts = Account.query.filter_by(user_id = current_user.id).all()
  loan_profiles = LoanProfile.query.filter_by(user_id = current_user.id).all()
  return render_template('customer_profile.html', profile=profile[0], accounts=accounts, loan_profiles=loan_profiles)

@app.route('/customer/loan_request', methods=['GET', 'POST'])
@roles_required('Customer')
def customer_loan_request():
  profile = Profile.query.filter_by(user_id = current_user.id).all()
  accounts = Account.query.filter_by(user_id = current_user.id).all()
  form = LoanStatusForm()
  status = "Not submitted"
  prediction = "No prediction yet"

  if form.validate_on_submit():
    status = "Submitted"
    
    annual_income = form.annual_income.data
    purpose = form.purpose_of_loan.data
    home_ownership = form.home_ownership.data
    term = form.term.data
    length_of_employment = form.emp_length_num.data
    time_of_employment = form.short_emp.data
    dti = form.dti.data
    percentage_available_credit = form.revol_util.data
    borrower_deliquency = form.last_delinq_none.data
    total_late_fees = form.total_rec_late_fee.data
    loan_amount = form.loan_amount

    randomForestAlgorithm = RandomForestAlgorithm(
      annual_income, purpose, home_ownership, term, length_of_employment, time_of_employment, dti, 
      percentage_available_credit, borrower_deliquency, total_late_fees
    )

    prediction = randomForestAlgorithm.process()

    if prediction == 'Eligible':
      loan_profile = LoanProfile(
        annual_income = annual_income,
        purpose_of_loan = purpose,
        home_ownership = home_ownership,
        term = term,
        length_of_employment = length_of_employment,
        time_of_employment = time_of_employment,
        dti = dti,
        loan_amount = loan_amount,
        percentage_available_credit = percentage_available_credit,
        borrower_deliquency = borrower_deliquency,
        total_late_fees = total_late_fees,
        user_id = current_user.id
      )

      db.session.add(loan_profile)
      db.session.commit()
      
      return redirect(url_for('customer_loan_confirmation'))
    else:
      return redirect(url_for('customer_loan_denial'))
    
  return render_template('customer_loan_request.html', profile=profile[0], form=form, status=status, prediction=prediction, accounts=accounts)

@app.route('/customer/loan_confirmation')
def customer_loan_confirmation():
  profile = Profile.query.filter_by(id = current_user.id).all()
  return render_template('customer_loan_confirmation.html', profile=profile[0])

@app.route('/customer/loan_denial')
def customer_loan_denial():
  profile = Profile.query.filter_by(id = current_user.id).all()
  return render_template('customer_loan_denial.html', profile=profile[0])

@app.route('/customer/exchange_rate_app')
def exchange_rate_app():
  profile = Profile.query.filter_by(id = current_user.id).all()
  return render_template('exchange_rate_app.html', profile=profile[0])

@app.errorhandler(404)
def page_not_found(e):
    return "404!"

def getAllCustomers(num):
    users_profiles = Profile.query.all()

    users = User.query.all()
    customer_ids = []
    customers = []

    for user in users:
      for role in user.roles:
        if role.name == 'Customer':
          customer_ids.append(user.id)

    for user_profile in users_profiles:
      if num == 'all':
        for id in customer_ids:
          if user_profile.user_id == id:
            customers.append(user_profile)
      else:
        for id in customer_ids[:num]:
          if user_profile.user_id == id:
            customers.append(user_profile)
    
    return customers
  
def getAllAdmins(num):
  users_profiles = Profile.query.all()

  users = User.query.all()
  admin_ids = []
  admins = []

  for user in users:
    for role in user.roles:
      if role.name == 'Admin':
        admin_ids.append(user.id)

  for user_profile in users_profiles:
    if num == 'all':
      for id in admin_ids:
        if user_profile.user_id == id:
          admins.append(user_profile)
    else:
      for id in admin_ids[:num]:
        if user_profile.user_id == id:
          admins.append(user_profile)
  
  return admins