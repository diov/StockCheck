from flask import render_template, redirect, flash
from flask import request, jsonify
from flask import url_for

from app import app
from app.forms import ReceiptForm
from model import item
from model.item import Stock, Receipt


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/stocks')
def show_stocks():
    return render_template('stocks.html')


@app.route('/stocks/details')
def show_detail_stocks():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 1, type=int)
    search = request.args.get('search', '', type=str)
    if search:
        pagination = Stock.query.filter(Stock.name.ilike("%{}%".format(search))) \
            .paginate(offset // limit + 1, per_page=limit, error_out=False)
    else:
        pagination = Stock.query.paginate(offset // limit + 1, per_page=limit, error_out=False)
    return jsonify(rows=[product.serialize for product in pagination.items], total=pagination.total)


@app.route('/product')
def fetch_product():
    search = request.args.get('search', '', type=str)
    if search:
        result = Stock.query.filter(Stock.name.ilike("%{}%".format(search))).all()
    else:
        result = ''
    return jsonify([product.serialize for product in result])


@app.route('/add_receipt', methods=['GET', 'POST'])
def add_receipt():
    form = ReceiptForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            products = form.products.data
            for product in products:
                data = {
                    'identifier': form.identifier.data,
                    'date': form.receipt_date.data,
                    'customer': form.customer.data,
                    'maker': form.maker.data,
                    'repository': form.repository.data,
                    'balance': form.balance.data,
                    'product_id': product.get('product_id'),
                    'name': product.get('product_name'),
                    'amount': product.get('amount'),
                    'price': product.get('price'),
                    'comment': product.get('comment'),
                    'sender': form.sender.data,
                    'handler': form.sender.data
                }
                message_dict = item.add_receipt(**data)
                if message_dict.get('status'):
                    flash(message=message_dict.get('message'), category='info')
                else:
                    flash(message=message_dict.get('message'), category='error')
        else:
            flash(form.errors)
        return redirect(url_for('add_receipt'))
    else:
        return render_template('add_receipt.html', title='添加发票', form=form)


@app.route('/receipts')
def show_receipts():
    return render_template('receipts.html', receipts=item.get_all_receipts())


@app.route('/receipts/details')
def show_receipts_details():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 1, type=int)
    search = request.args.get('search', '', type=str)
    if search:
        pagination = Receipt.query.filter(Receipt.customer.ilike("%{}%".format(search))) \
            .paginate(offset // limit + 1, per_page=limit, error_out=False)
    else:
        pagination = Receipt.query.paginate(offset // limit + 1, per_page=limit, error_out=False)
    return jsonify(rows=[receipt.serialize for receipt in pagination.items], total=pagination.total)
