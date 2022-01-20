"""Creational patterns"""
from copy import deepcopy
from quopri import decodestring

from .cbv import FileWriter, Subject


class User:
    def __init__(self, name):
        self.name = name


# владелец (админ, продавец)
class Owner(User):
    pass


# клиент (покупатель, заказчик)
class Client(User):
    def __init__(self, name):
        self.products = []
        super().__init__(name)


class UserFactory:
    types = {
        'owner': Owner,
        'client': Client,
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class ProductPrototype:
    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.products.append(self)
        self.clients = []
        super().__init__()

    def __getitem__(self, item):
        return self.clients[item]

    def add_client(self, client: Client):
        self.clients.append(client)
        client.products.append(self)
        self.notify()


# Вещественное
class ThingProduct(Product):
    pass


# Бобровое
class BeaverProduct(Product):
    pass


# Нереальное
class FantasyProduct(Product):
    pass


# Невыполнимое
class ImpossibleProduct(Product):
    pass


class ProductFactory:
    types = {
        'thing': ThingProduct,
        'beaver': BeaverProduct,
        'fantasy': FantasyProduct,
        'impossible': ImpossibleProduct,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def product_count(self):
        result = len(self.products)
        if self.category:
            result += self.category.product_count()
        return result


class Engine:
    def __init__(self):
        self.owners = []
        self.clients = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id={id}')

    @staticmethod
    def create_product(type_, name, category):
        return ProductFactory.create(type_, name, category)

    def get_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        return None

    def get_client(self, name) -> Client:
        for item in self.clients:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'utf-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('utf-8')


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log: {text}'
        self.writer.write(text)
