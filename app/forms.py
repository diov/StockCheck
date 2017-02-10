from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, DecimalField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product_id = StringField(u'商品编号', validators=[DataRequired(u'编号不能为空')])
    product_name = StringField(u'商品名称', validators=[DataRequired(u'名称不能为空')])
    amount = IntegerField(u'数量', validators=[DataRequired(u'数量不能为空')])
    price = DecimalField(u'金额', validators=[DataRequired(u'金额不能为空')])
    comment = StringField(u'备注')


class ReceiptForm(FlaskForm):
    receipt_date = DateField(u'日期', validators=[DataRequired(u'日期不能为空')])
    customer = StringField(u'客户', validators=[DataRequired(message=u'客户不能为空')])
    identifier = StringField(u'编号', validators=[DataRequired(message=u'编号不能为空')])
    maker = StringField(u'制单人', validators=[DataRequired(message=u'制单人不能为空')])
    repository = SelectField(u'仓库', validators=[DataRequired()], choices=[('主仓库', '主仓库'), ('次仓库', '次仓库')])
    balance = SelectField(u'结算方式', validators=[DataRequired()], choices=[('货到付款', '货到付款'), ('款到发货', '款到发货')])
    products = FieldList(FormField(ProductForm), min_entries=1)
    sender = StringField(u'发货人')
    handler = StringField(u'经手人')
