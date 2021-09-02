from flask import render_template, request, Blueprint, redirect, url_for
from invoice.forms import ReportForm,MainForm , AddItemForm, RecieveForm, AddClientForm
from invoice.models import Sales, Purchase, Items, Client
from invoice.helper_functions import breakdown, timeview, choice, sum_bydays, extract, paid
from flask_login import login_user, login_required, logout_user, current_user
import datetime
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from invoice import login_manager, db

application = Blueprint('application', __name__)

####################################
######### Dashboard Page View ######
####################################


@application.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ReportForm()
    month = dt.today().month
    month_list = [0, 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    sitems = extract(Sales)
    pitems = extract(Purchase)
    s_totaldata = sum_bydays(month, Sales)[0]
    s_paiddata = sum_bydays(month, Sales)[1]
    s_remaindata = sum_bydays(month, Sales)[2]
    p_totaldata = sum_bydays(month, Purchase)[0]
    p_paiddata = sum_bydays(month, Purchase)[1]
    p_remaindata = sum_bydays(month, Purchase)[2]

    smonth_total = timeview(sitems)[0]
    smonth_paid = timeview(sitems)[1]
    smonth_remain = timeview(sitems)[2]
    pmonth_total = timeview(pitems)[0]
    pmonth_paid = timeview(pitems)[1]
    pmonth_remain = timeview(pitems)[2]

    labels = list(range(1, len(s_totaldata)+1))

    return render_template('dashboard.html', form=form, sitems=sitems, pitems=pitems,
                        smonth_total=smonth_total, smonth_paid=smonth_paid, smonth_remain=smonth_remain,
                        pmonth_total=pmonth_total, pmonth_paid=pmonth_paid, pmonth_remain=pmonth_remain,
                        s_totaldata=s_totaldata, s_paiddata=s_paiddata, s_remaindata=s_remaindata,
                        p_totaldata=p_totaldata, p_paiddata=p_paiddata, p_remaindata=p_remaindata, labels=labels, month_name=month_list[month], title='Dashboard')


@application.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    form = MainForm()
    if form.submit.data:
        name = form.name.data
        item = form.item.data[:-2]
        description = form.description.data[:-2]
        alternate_quantity = form.alternate_quantity.data[:-2]
        quantity = form.quantity.data[:-2]
        rate = form.rate.data[:-2]
        per = form.per.data[:-2]
        amount = form.amount.data[:-2]
        total_amount = form.total_amount.data
        paid_amount = form.paid_amount.data
        discount = form.discount.data
        remaning_amount = form.remaning_amount.data

        sales = Sales(admin_id=current_user.id, name=name, item=item, description=description,
        alternate_quantity=alternate_quantity, quantity=quantity, rate=rate, per=per, amount=amount,
        total_amount=total_amount, discount=discount, paid_amount=paid_amount, remaning_amount=remaning_amount)

        db.session.add(sales)
        db.session.commit()
        return redirect(url_for('application.salesvoucher'))
    return render_template('desc.html', form=form, title='Sales')

@application.route('/purchases', methods=['GET', 'POST'])
@login_required
def purchases():
    form = MainForm()
    if form.submit.data:
        name = form.name.data
        item = form.item.data[:-2]
        description = form.description.data[:-2]
        alternate_quantity = form.alternate_quantity.data[:-2]
        quantity = form.quantity.data[:-2]
        rate = form.rate.data[:-2]
        per = form.per.data[:-2]
        amount = form.amount.data[:-2]
        total_amount = form.total_amount.data
        paid_amount = form.paid_amount.data
        remaning_amount = form.remaning_amount.data
        purchase = Purchase(admin_id=current_user.id, name=name, item=item, description=description,
        alternate_quantity=alternate_quantity, quantity=quantity, rate=rate, per=per, amount=amount,
        total_amount=total_amount, paid_amount=paid_amount, remaning_amount=remaning_amount)
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('application.purchasevoucher'))
    return render_template('desc.html', form=form, title='Purchase')

@application.route('/salesvoucher')
@login_required
def salesvoucher(last_entry = 0):
    if last_entry == 0:
        last_entry=Sales.query.order_by(Sales.id.desc()).first()
    else:
        last_entry = last_entry
    name = last_entry.name
    item = last_entry.item.split('/n')
    description = last_entry.description.split('/n')
    alternate_quantity = last_entry.alternate_quantity.split('/n')
    total_alternate_quantity = sum([float(i) for i in alternate_quantity])
    quantity = last_entry.quantity.split('/n')
    total_quantity = sum([float(i) for i in quantity])
    rate = last_entry.rate.split('/n')
    per = last_entry.per.split('/n')
    amount = last_entry.amount.split('/n')
    total_amount = last_entry.total_amount
    discount = last_entry.discount
    paid_amount = last_entry.paid_amount
    remaning_amount = int(total_amount)-int(paid_amount)-int(discount)
    item_range = list(range(9))
    item_len = len(item)

    return render_template('sales/invoice.html', name=name, item_len=item_len, item_range=item_range, last_entry=last_entry, item=item,
    description=description, alternate_quantity=alternate_quantity, total_alternate_quantity=total_alternate_quantity,
    quantity=quantity, total_quantity=total_quantity, rate=rate, per=per, amount=amount,
    total_amount=total_amount, discount=discount, paid_amount=paid_amount, remaining_amount=remaning_amount,
    title='Sales | Invoice')


@application.route('/purchasevoucher')
@login_required
def purchasevoucher(last_entry=0):
    if last_entry == 0:
        last_entry=Purchase.query.order_by(Purchase.id.desc()).first()
    else:
        last_entry = last_entry
    name = last_entry.name
    item = last_entry.item.split('/n')
    description = last_entry.description.split('/n')
    alternate_quantity = last_entry.alternate_quantity.split('/n')
    total_alternate_quantity = sum([float(i) for i in alternate_quantity])
    quantity = last_entry.quantity.split('/n')
    total_quantity = sum([float(i) for i in quantity])
    rate = last_entry.rate.split('/n')
    per = last_entry.per.split('/n')
    amount = last_entry.amount.split('/n')
    total_amount = last_entry.total_amount
    paid_amount = last_entry.paid_amount
    remaning_amount = int(total_amount)-int(paid_amount)
    item_range = list(range(9))
    item_len = len(item)

    return render_template('sales/invoice.html', name=name, item_len=item_len, item_range=item_range, last_entry=last_entry, item=item,
    description=description, alternate_quantity=alternate_quantity, total_alternate_quantity=total_alternate_quantity,
    quantity=quantity, total_quantity=total_quantity, rate=rate, per=per, amount=amount,
    total_amount=total_amount, discount=0, paid_amount=paid_amount, remaining_amount=remaning_amount,
    title='Purchase | Invoice')


@application.route('/salesentries', methods=["GET", "POST"])
@login_required
def salesentries():
    form = ReportForm()
    items = extract(Sales)
    return render_template('sales/salesentries.html', items=items, form=form, title='Sales')


@application.route('/purchaseentries',methods=["GET","POST"])
@login_required
def purchaseentries():
    form = ReportForm()
    items = extract(Purchase)
    return render_template('purchase/purchaseentries.html', items=items,form=form, title='Purchase')


@application.route('/<int:id>/salesvoucher', methods=["GET", "POST"])
@login_required
def voucher_id(id):
    return salesvoucher(last_entry=Sales.query.filter_by(id=id).first())


@application.route('/<int:id>/purchase',methods=["GET","POST"])
@login_required
def pvoucher_id(id):
   return purchasevoucher(last_entry=Purchase.query.filter_by(id=id).first())


@application.route('/<costumer_name>/costumer', methods=["GET", "POST"])
@login_required
def profile(costumer_name):
    form1 = RecieveForm()
    total_amount = 0
    paid_amount = 0
    remaning_amount = 0
    client = Client.query.filter_by(
        companyname=costumer_name).first()
    items = Sales.query.filter_by(
        name=costumer_name)
    for i in items:
        total_amount += i.total_amount
        paid_amount += i.paid_amount
        remaning_amount += i.remaning_amount
    if form1.submit.data:
        paid(costumer_name, Sales, form1)
    return render_template('profile.html', costumer_name=costumer_name, items=items, total_amount=total_amount, 
    paid_amount=paid_amount, remaning_amount=remaning_amount, title = costumer_name,client = client, form1=form1)


@application.route('/<int:id>/sdelete', methods=["GET", "POST"])
@login_required
def delete_sales(id):
    entry = Sales.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('salesentries'))


@application.route('/<seller_name>/seller',methods=["GET","POST"])
@login_required
def sellerprofile(name):
    form1 = RecieveForm()
    total_amount = 0
    paid_amount = 0
    remaning_amount = 0
    items = Purchase.query.filter_by(
        name=name)
    for i in items:
        total_amount += i.total_amount
        paid_amount += i.paid_amount
        remaning_amount += i.remaning_amount
        name = i.name
    if form1.validate_on_submit():
        paid(name, Purchase, form1)
    return render_template('profile.html', costumer_name=name, items=items, total_amount=total_amount, 
    paid_amount=paid_amount, remaning_amount=remaning_amount, title = name, form1=form1)

@application.route('/<int:id>/pdelete',methods=["GET","POST"])
@login_required
def delete_purchase(id):
    entry=Purchase.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('purchaseentries'))

@application.route('/add_item',methods=['GET','POST'])
def add_item():
    form=AddItemForm()
    if form.validate_on_submit():
        item_name=form.item_name.data
        item_brand=form.item_brand.data
        item_category=form.item_category.data
        item_price=form.item_price.data
        item_quantity=form.item_quantity.data
        item=Items(item_name=item_name,item_brand=item_brand,item_category=item_category,item_price=item_price,item_quantity=item_quantity)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('item_list'))
    return render_template('items/add_items.html',form=form)

@application.route('/item_list',methods=['GET','POST'])
def item_list():
    items =Items.query.all()
    return render_template('items/item_inventory.html', items=items)


@application.route('/client', methods = ['GET', 'POST'])
def client():
    costumer = Client.query.all()
    return render_template('client_list.html', items = costumer)



@application.route('/add_client', methods = ['GET', 'POST'])
def add_costumers():
    form  = AddClientForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        companyname = form.companyname.data
        role = form.role.data
        email = form.email.data
        primary_no = form.primary_phone.data
        secondary_no = form.secondary_phone.data
        address = form.address.data
        pan_no = form.pan_no.data
        costumer = Client(firstname=firstname, lastname=lastname, companyname = companyname, role=role, email=email, 
        primary_no=primary_no, secondary_no=secondary_no, address=address, pan_no=pan_no)
        db.session.add(costumer)
        db.session.commit()
        return redirect(url_for('application.client'))

    return render_template('add_costumer.html', form = form)