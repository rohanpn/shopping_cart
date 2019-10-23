
import json
import os
import sys
import typing
from importlib.machinery import SourceFileLoader

a_bc = SourceFileLoader(os.path.dirname(os.path.abspath(sys.argv[0])) , "abc.py").load_module()

CONFIG_DIR = "json"


class ShoppingCart(a_bc.ShoppingCart):

    def __init__(self):
        self._items = dict()

    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

    def print_receipt(self) -> typing.List[str]:
        lines = []
        total_price = 0
        try:
            for item in self._items.items():

                price = self._get_product_price(item[0]) * item[1]
                total_price += price
                price_string = "€%.2f" % price

                lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)

            lines.append("Total Price = €%.2f" % total_price)

            return lines
        except Exception as ex:
            print("Error : ", ex)

    def print_receipt_with_currencies(self) -> typing.List[str]:
        lines = []
        total_price = 0
        currency_rate = self._get_currency_rate()
        try:
            for item in self._items.items():

                price = self._get_product_price(item[0]) * item[1]
                total_price += price
                price_list = list()
                for currency in currency_rate:
                    price_list.append(currency["currency"] + "%.2f " % (price * currency['rate']))

                lines.append(item[0] + " - " + str(item[1]) + ' - ' + "/ ".join(price_list))
            final_price = list()
            for currency in currency_rate:
                final_price.append(currency["currency"] + "%.2f" % (total_price * currency['rate']))

            lines.append("Total Price = " + " / ".join(final_price))

            return lines
        except Exception as ex:
            print("Error : ", ex)

    def _get_currency_rate(self) -> list:
        currency_data = list()
        with open(os.path.join(CONFIG_DIR, "currency.json"), "rb") as fh:
            file_data = fh.read()
            currency_data = json.loads(file_data)

        return currency_data

    def _read_product_data(self):
        data = str()
        with open(os.path.join(CONFIG_DIR, "data.json"), "rb") as fh:
            data = fh.read()
        return json.loads(data)

    def _get_product_price(self, product_code: str) -> float:
        price = 0.0
        data = str()
        try:
            parsed_data = self._read_product_data()
            for code in parsed_data:
                if product_code == code['product_code']:
                    return code['price']
            raise
        except Exception as ex:
            print("Item not present in source data")

    def display_product_price(self, product_code) -> bool:
        try:
            product_price = list()
            price = self._get_product_price(product_code)
            currency_rate = self._get_currency_rate()
            for currency in currency_rate:
                product_price.append(currency["currency"] + "%.2f" % (price * currency['rate']))
            print("Price of %s : " % (product_code) + "  / ".join(product_price))
        except Exception:
            return False

def main():

    if not len(sys.argv) > 0:
        exit()
    global CONFIG_DIR

    CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "json")

    shop_cart = ShoppingCart()
    shop_cart.display_product_price("apple")
    shop_cart.add_item("apple", 1)
    shop_cart.add_item("apple", 1)
    shop_cart.add_item("banana", 2)
    print("\nTotal Price : ", shop_cart.print_receipt())
    print("\nTotal Price in multiple currencies : \n", shop_cart.print_receipt_with_currencies())



if __name__ == "__main__":
    main()