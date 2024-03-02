from flask import Flask, render_template, request, redirect, url_for, Blueprint
from wmgzon.db import get_db

basket = Blueprint('basket', __name__)

@basket.route('/basket/<int:product_id>', methods=['GET', 'POST'])
def add_to_basket(product_id):
    print("this is ihtihsighdihg", product_id)
    cursor = get_db().cursor()

    # Execute SQL query to fetch product details
    cursor.execute(
        'SELECT p.id, p.title, p.price, p.description, p.image_filename'
        ' FROM product p'
        ' WHERE p.id = ?',
        (product_id,))

    product = cursor.fetchone()
    #
    #print("product +++= ", product)
    # product= products.get(product_id)

    # if request.method == 'POST':
    #     if product:
    #         quantity = int(request.form['quantity'])
    #         product['quantity'] = quantity
    #         basket.append(productid)
    #         return redirect(url_for('index'))
    return render_template('landingpage/basket.html', product=product)

@basket.route('/basket')
def view_basket():
    total_price = sum(product['price'] * product.get('quantity', 1) for product in basket)
    return render_template('basket.html', basket=basket, total_price=total_price)
