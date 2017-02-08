from app import db


class Stock(db.Model):
    # 表名
    __tablename__ = 'stock'

    # 表结构
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(20))
    unit = db.Column(db.String(10))
    factory_name = db.Column(db.String(20))
    purchase_price = db.Column(db.FLOAT)
    sale_price = db.Column(db.FLOAT)
    amount = db.Column(db.INTEGER)

    @property
    def serialize(self):
        return {
            'stock_id': self.id,
            'name': self.name,
            'unit': self.unit,
            'factory_name': self.factory_name,
            'purchase_price': self.purchase_price,
            'sale_price': self.sale_price,
            'amount': self.amount
        }

    def __repr__(self):
        return "<商品(名称={}, 单位={}, 厂家={}, 库存量={}, 进价={}, 售价={})>" \
            .format(self.name, self.unit, self.factory_name, self.amount, self.purchase_price, self.sale_price)


class Receipt(db.Model):
    # 表名
    __tablename__ = 'receipt'

    # 表结构
    id = db.Column(db.INTEGER, primary_key=True)
    identifier = db.Column(db.String(20))  # 编号
    date = db.Column(db.DateTime)  # 日期
    customer = db.Column(db.String(20))  # 客户
    maker = db.Column(db.String(20))  # 制单人
    repository = db.Column(db.String(20))  # 发货仓库
    balance = db.Column(db.String(20))  # 结算方式
    product_id = db.Column(db.String(20))  # 商品编号
    name = db.Column(db.String(20))  # 商品名称
    amount = db.Column(db.INTEGER)  # 数量
    price = db.Column(db.FLOAT)  # 金额
    comment = db.Column(db.String(30))  # 备注
    sender = db.Column(db.String(20))  # 发货人
    handler = db.Column(db.String(20))  # 经手人

    @property
    def serialize(self):
        product = session.query(Stock).filter(Stock.id == self.product_id).first()
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'customer': self.customer,
            'receipt_id': self.identifier,
            'maker': self.maker,
            'repository': self.repository,
            'balance': self.balance,
            'product_name': product.name,
            'unit': product.unit,
            'amount': self.amount,
            'sale_price': product.sale_price,
            'price': self.price,
            'comment': self.comment,
            'sender': self.sender,
            'handler': self.handler
        }

    def __repr__(self):
        return "<Receipt(identifier={}, date={}, customer={}, maker={}, repository={}, balance={}, product_id={}, " \
               "name={}, amount={}, price={}, comment={}, sender={}, handler={}>" \
            .format(self.identifier, self.date, self.customer, self.maker, self.repository, self.balance,
                    self.product_id,
                    self.name, self.amount, self.price, self.comment, self.sender, self.handler)


# 初始化数据库连接:
db.create_all()
# 创建Session类型:
session = db.session


def import_stock():
    import xlrd

    with xlrd.open_workbook('./source/realtime.xls') as book:
        product_sheet = book.sheet_by_index(2)

        for rx in range(1, product_sheet.nrows):
            item = product_sheet.row(rx)
            # 创建新Stock对象:
            new_stock = Stock(name=item[0].value, factory_name=item[4].value, unit=item[1].value,
                              purchase_price=item[2].value if 0 != item[2].ctype else 0.0,
                              sale_price=item[3].value if 0 != item[3].ctype else 0.0)
            # 添加到session:
            session.add(new_stock)
            # 提交即保存到数据库:
            session.commit()

        stock_sheet = book.sheet_by_index(0)

        for rx in range(1, stock_sheet.nrows):
            item = stock_sheet.row(rx)
            session.query(Stock).filter(Stock.name == item[1].value) \
                .update({"amount": item[2].value if item[2].ctype != 0 else 0})
            session.commit()

        session.close()


def get_all_stock():
    stocks = session.query(Stock)
    session.close()
    return stocks


def get_all_receipts():
    receipts = session.query(Receipt)
    session.close()
    return receipts


def add_receipt(**kwargs):
    identifier = kwargs.get('identifier')  # 编号
    date = kwargs.get('date')  # 日期
    customer = kwargs.get('customer')  # 客户
    maker = kwargs.get('maker')  # 制单人
    repository = kwargs.get('repository')  # 发货仓库
    balance = kwargs.get('balance')  # 结算方式
    product_id = kwargs.get('product_id')  # 商品编号
    name = kwargs.get('name')  # 商品名称
    amount = int(kwargs.get('amount'))  # 数量
    price = float(kwargs.get('price'))  # 金额
    comment = kwargs.get('comment')  # 备注
    sender = kwargs.get('sender')  # 发货人
    handler = kwargs.get('handler')  # 经手人

    if not date:
        from datetime import datetime
        date = datetime.today()

    if Receipt.query.filter(identifier == identifier):
        return {'status': False, 'message': u'已经存在相同编号的发票！'}
    else:
        new_receipt = Receipt(identifier=identifier, date=date, customer=customer, maker=maker, repository=repository,
                              balance=balance, product_id=product_id, name=name, amount=amount, price=price,
                              comment=comment, sender=sender, handler=handler)

        try:
            session.add(new_receipt)
            stock = session.query(Stock).filter(Stock.id == product_id).first()
            stock.amount -= amount
            session.add(stock)
            # 提交即保存到数据库:
            session.commit()
            return {'status': True, 'message': u'添加发票成功！'}
        except:
            return {'status': False, 'message': u'添加发票失败'}
        finally:
            session.close()
