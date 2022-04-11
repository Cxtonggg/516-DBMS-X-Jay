from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import IntegerField, SubmitField, StringField, TextAreaField
from .models.product import Product
from .models.feedbackToProduct import feedbackToProduct
from wtforms.validators import ValidationError, DataRequired, NumberRange
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/productdetails/<int:pid>', methods=['GET', 'POST'])
def details(pid):# get all available products for sale:
    product = Product.get(pid)
    seller_info = Product.getSellerInfo(pid)
    return render_template('productdetails.html', avail_products = [product],seller_info = seller_info)



@bp.route('/cart', methods=['GET', 'POST'])
def cart():# get all available products for sale:
    # TODO: get products & quantities in user's cart
    return render_template('cart.html', cart = [])
    
@bp.route('/addtocart/<sid>/<pid>', methods=['GET', 'POST'])
def addToCart(sid,pid):
    #TODO: to implement an interface to add # quantities of product(pid) from the seller(sid) to cart
    return render_template('addToCart.html', sid=sid, pid=pid)


class feedbackToProductForm(FlaskForm):
    ratings = IntegerField('Please rate this product from 1-5',
                            validators=[DataRequired(), NumberRange(min=1, max = 5, message='exceeds valid range')])
    feedback = TextAreaField('Please write your feedback to this product', validators=[DataRequired()])
    submit = SubmitField('submit')

@bp.route('/writefeedback/<pid>', methods=['GET', 'POST'])
def writeFeedback(pid):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = feedbackToProductForm()
    uid = current_user.id
    if form.validate_on_submit():
        #send feedback to db
        text = form.feedback.data
        ratings = form.ratings.data
        result = feedbackToProduct.AddFeedbackToProduct(uid, pid, ratings, text)
        if not result:
            flash('sorry, something went wrong')
        else:
            flash('submit already')
            product = Product.get(pid)
            seller_info = Product.getSellerInfo(pid)
            return render_template('productdetails.html',avail_products=[product],seller_info=seller_info)
    return render_template('feedbackToProduct.html',form=form, pid=pid)

