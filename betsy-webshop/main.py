__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
import os


def main():
    populate_test_database()


def populate_test_database():
    # Initialize database
    db.connect()
    db.create_tables([Product, User, Transaction, ProductOwner, ProductTag, Tag])
    
    # Create users
    users = [
        ["Bob", "Amsterdam", "222-456"],
        ["Dennis", "Hilversum", "123-456"],
        ["Christa", "Leiden", "423-734"],
        ["Momo", "Linschoten", "888-888"],
        ["Bonnie", "Leiderdorp", "359-728"],
    ]
    for user in users:
        create_user(user)

    
    # Add products
    products = [
        ["Vespa", "Not used since 1999", 1999.95, 1, "Scooter"],
        ["Nike Air", "The classic", 60.00, 5, "Shoes"],
        ["Jeans", "Very now", 88.30, 4, "Pants"],
        ["Short Jeans", "Very now", 88.30, 4, "Pants"],
    ]
    add_product_to_catalog(3, products[0])
    add_product_to_catalog(1, products[1])
    add_product_to_catalog(4, products[2])
    add_product_to_catalog(4, products[3])

    # close database
    db.close()


def delete_database():
    cwd = os.getcwd()
    database = "webshop.db"
    database_path = os.path.join(cwd, database)
    if os.path.exists(database_path):
        os.remove(database_path)


def search(term):
    """
    Search products

    >>> search("Jean")
    We have Jeans.
    We have Short Jeans.
    """

    query = Product.select(fn.lower(Product.name), Product.id)
    product_found = []
    product_name = []
    for item in query:
        if term.lower() in item.name:
            product_found.append(item.id)
    for product in product_found:
        query = (Product.select(Product.name, Product.id)
         .where(Product.id == product))
        for item in query:
            product_name.append(item.name)
    for product in product_name:
        print(f"We have {product}.")     


def list_user_products(user_id):
    """
    Listing products by user:

    >>> list_user_products(4)
    Jeans
    Short Jeans
    """
    query = (Product
             .select(Product.name, Product.id)
             .join(ProductOwner)
             .where(ProductOwner.user_id == user_id)
             )
    for item in query:
        print(item.name)


def list_products_per_tag(tag_id):
    """
    Listing products by tag:

    >>> list_products_per_tag(3)
    Jeans
    Short Jeans
    """
    query = (
        Product
        .select(Product.name, Product.id)
        .join(ProductTag)
        .where(ProductTag.tag_id == tag_id)
    )
    for item in query:
        print(item.name)


def create_user(user):
    User.get_or_create(
        name = user[0],
        address = user[1],
        billing_info = user[2]
    )


def add_product_to_catalog(user_id, product):
    # Create tag
    tag = product[4]
    Tag.get_or_create(
        name = tag
    )

    # create product
    Product.get_or_create(
        name = product[0],
        description = product[1],
        price = product[2],
        stock_quantity = product[3],
        tag = Tag.get(Tag.name == product[4]),
        )
    
    # create connection between user and product
    user = User.get(User.id == user_id)
    new_product = Product.get(Product.name == product[0])
    ProductOwner.create(user_id=user, product_id=new_product)

    # Create connection between product and tag
    get_tag = Tag.get(Tag.name == tag)
    ProductTag.create(tag_id = get_tag, product_id = new_product)


def update_stock(product_id, new_quantity):
    """
    # Test update stock

    >>> update_stock(2, 55)
    ('Nike Air', 55)
    """
    (Product.update(stock_quantity = new_quantity)
     .where(Product.id == product_id)
     .execute()
     )
    query = Product.select(Product.id, Product.name).where(Product.id == product_id)
    product = [item.name for item in query]
    query = Product.select(Product.id, Product.stock_quantity).where(Product.id == product_id)
    quantity = [item.stock_quantity for item in query]
    return (product[0], quantity[0])


def purchase_product(product_id, buyer_id, quantity):
    """
    Purchase product

    >>> purchase_product(2, 3, 2)
    """
    query = Product.select(Product.id, Product.stock_quantity).where(Product.id == product_id)
    new_stock = [item.stock_quantity - quantity for item in query]
    
    if new_stock[0] > 0:
        update_stock(product_id, new_stock[0])
        transaction(product_id, buyer_id, quantity)
    elif new_stock[0] == 0:
        remove_product(product_id)
        transaction(product_id, buyer_id, quantity)
    elif new_stock[0] < 0:
        return 'Error: Not enough stock.'
    

def transaction(product_id, buyer_id, quantity):
    """
    Transaction

    >>> transaction(2, 3, 2)
    [<User: 3>...]
    """
    Transaction.create(buyer = buyer_id, product = product_id, quantity = quantity)
    query = Transaction.select().where(Transaction.buyer == buyer_id)
    transaction = [item.buyer for item in query]
    return transaction



def remove_product(product_id):
    """
    Delete product

    >>> remove_product(1)
    'Product: 1 deleted.'
    """
    Product.delete().where(Product.id == product_id).execute()
    return f"Product: {product_id} deleted."


if __name__ == "__main__":
    main()
