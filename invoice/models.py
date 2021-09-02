from invoice import db,login_manager
import datetime
from flask import redirect, url_for
from datetime import datetime as dt
from flask_admin.contrib.sqla import ModelView
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user,login_required,logout_user,current_user

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    __tablename__='admin'
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.Text)
    lastname=db.Column(db.Text)
    username=db.Column(db.Text,unique=True,index=True)
    password_hash=db.Column(db.Text)

    def __init__(self,firstname,lastname,username,password):
        self.firstname=firstname
        self.lastname=lastname
        self.username=username
        self.password_hash=generate_password_hash(password) 



    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        

class Items(db.Model):

    __tablename__='items'
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.DateTime(),nullable=False,default=datetime.date.today())
    item_name=db.Column(db.Text)
    item_category=db.Column(db.Text)
    item_brand=db.Column(db.Text)
    item_quantity=db.Column(db.Integer)
    item_price=db.Column(db.Integer)

    def __init__(self,item_name,item_category,item_brand,item_price,item_quantity):
        self.item_name=item_name
        self.item_brand=item_brand
        self.item_category=item_category
        self.item_quantity=item_quantity
        self.item_price=item_price


class Sales(db.Model):
    __tablename__='sales'
    admin=db.relationship(User)
    id=db.Column(db.Integer,primary_key=True)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.date.today())
    name = db.Column(db.Text,nullable=False, default='Retail')
    item = db.Column(db.String,nullable=False)
    description = db.Column(db.String, nullable = False)
    alternate_quantity = db.Column(db.String, nullable = False)
    quantity = db.Column(db.String,nullable=False)
    rate = db.Column(db.String,nullable=False)
    per = db.Column(db.String, nullable = False)
    amount = db.Column(db.String,nullable = False)
    total_amount = db.Column(db.Integer,nullable=False)
    discount = db.Column(db.Integer,nullable=True, default=0)
    paid_amount = db.Column(db.Integer)
    remaning_amount = db.Column(db.Integer,default=0)
    
    def __init__(self, admin_id, item, name, description, alternate_quantity, quantity, rate, per, amount, total_amount,
    paid_amount, discount, remaning_amount):
        self.admin_id=admin_id
        self.item = item
        self.name = name
        self.description = description
        self.alternate_quantity = alternate_quantity
        self.quantity = quantity
        self.rate = rate
        self.per = per
        self.amount=amount
        self.total_amount = total_amount
        self.paid_amount = paid_amount
        self.remaning_amount = remaning_amount
        self.discount = discount

class Purchase(db.Model):
    __tablename__='purchase'
    admin=db.relationship(User)
    id=db.Column(db.Integer,primary_key=True)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.date.today())
    name = db.Column(db.Text,nullable=False)
    item = db.Column(db.String,nullable=False)
    description = db.Column(db.String, nullable = False)
    alternate_quantity = db.Column(db.String, nullable = False)
    quantity = db.Column(db.String,nullable=False)
    rate = db.Column(db.String,nullable=False)
    per = db.Column(db.String, nullable = False)
    amount = db.Column(db.String,nullable = False)
    total_amount = db.Column(db.Integer,nullable=False)
    paid_amount = db.Column(db.Integer)
    remaning_amount = db.Column(db.Integer,default=0)
    
    def __init__(self, admin_id, item, name, description, alternate_quantity, quantity, rate, per, amount, total_amount,
    paid_amount, remaning_amount):
        self.admin_id=admin_id
        self.item = item
        self.name = name
        self.description = description
        self.alternate_quantity = alternate_quantity
        self.quantity = quantity
        self.rate = rate
        self.per = per
        self.amount=amount
        self.total_amount = total_amount
        self.paid_amount = paid_amount
        self.remaning_amount = remaning_amount


class Client(db.Model):
    __tablename__='costumer'
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String,nullable = False)
    lastname = db.Column(db.String,nullable = False)
    companyname = db.Column(db.String,unique=True,index=True)
    role = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable = True)
    primary_no = db.Column(db.String,nullable = False)
    secondary_no = db.Column(db.String,nullable = True)
    address = db.Column(db.Text, nullable = True)
    pan_no  = db.Column(db.String,nullable = True)
    def __init__(self,firstname,lastname,companyname, role, email, primary_no, secondary_no, address, pan_no):
        self.firstname = firstname
        self.lastname = lastname
        self.companyname = companyname
        self.role = role
        self.email = email
        self.primary_no = primary_no
        self.secondary_no = secondary_no
        self.address = address
        self.pan_no = pan_no


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username=='pujafancy'
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))