from peewee import *

db = SqliteDatabase("webshop.db")


# Models go here

class BaseModel(Model):
    class Meta:
        database = db


class Tag(BaseModel):
    name = CharField(unique=True)


class Product(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    price = DecimalField(decimal_places=2, auto_round=True)
    stock_quantity = IntegerField()
    tag = ForeignKeyField(Tag)


class ProductTag(BaseModel):
    tag_id = ForeignKeyField(Tag)
    product_id = ForeignKeyField(Product)


class User(BaseModel):
    name = CharField(unique=True)
    address = CharField()
    billing_info = CharField()


class Transaction(BaseModel):
    buyer = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity = IntegerField()


class ProductOwner(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
