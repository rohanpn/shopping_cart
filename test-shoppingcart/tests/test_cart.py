from __future__ import absolute_import

from shoppingcart.cart import ShoppingCart


def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1)
    cart.add_item("banana", 2)
    receipt = cart.print_receipt()
    assert receipt[0] == "apple - 1 - €1.00"


def test_total_price():
    cart = ShoppingCart()
    cart.add_item("apple", 1)

    receipt = cart.print_receipt()
    assert receipt[1] == "Total Price = €1.00"


def test_add_multiple_items():
    cart = ShoppingCart()
    cart.add_item("apple", 2)
    cart.add_item("banana", 2)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 2 - €2.00"
    assert receipt[1] == "banana - 2 - €2.20"


def test_total_price_with_multiple_currencies():
    cart = ShoppingCart()
    cart.add_item("apple", 1)
    cart.add_item("apple", 1)
    cart.add_item("banana", 2)
    receipt = cart.print_receipt_with_currencies()
    assert receipt[-1] == "Total Price = €4.20 / $4.58 / £3.86 / INR327.60"

