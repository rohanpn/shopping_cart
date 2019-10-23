
import abc
import typing


class ShoppingCart(abc.ABC):

    def add_item(self, product_code : str, quantity : int):
        pass

    def print_receipt(self):
        return []
