import stripe
from config.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY



def create_stripe_product(course):
    product = stripe.Product.create(name=course.name)
    return product


def create_stripe_price(product, amount):
    product_id = product.get('id')
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product_id,
    )
    return price


def create_stripe_checkout_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000",
        line_items=[{"price":price.get('id') , "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get('url')