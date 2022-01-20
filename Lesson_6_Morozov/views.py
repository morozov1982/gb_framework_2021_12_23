from moroz_framework.templator import render
from components.models import Engine, Logger
from components.decorators import AppRoute, Debug
from components.cbv import EmailNotifier, SmsNotifier, CreateView, ListView, \
    BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html')


# наверное позже удалю ибо не использую ;-)
class ProductCatalog:
    @Debug(name='ProductCatalog')
    def __call__(self, request):
        return '200 OK', render('products.html')


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 Page not Found'


@AppRoute(routes=routes, url='/create-product/')
class CreateProduct:
    category_id = -1

    @Debug(name='CreateProduct')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None

            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                product = site.create_product('thing', name, category)

                product.observers.append(email_notifier)
                product.observers.append(sms_notifier)

                site.products.append(product)

            return '200 OK', render('product-list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-product.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/products/')
class ProductsList:
    @Debug(name='ProductsList')
    def __call__(self, request):
        logger.log('Каталог продуктов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('product-list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('category-list.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/categories/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


# Тоже решил переписать, лишним не будет ;-) Пока работает некорректно
@AppRoute(routes=routes, url='/copy-product/')
class CopyProduct:
    @Debug(name='CopyProduct')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_product = site.get_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render('product-list.html',
                                    objects_list=site.products,
                                    name=new_product.category.name,
                                    id=new_product.category.id)
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/create-client/')
class ClientCreateView(CreateView):
    template_name = 'create_client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('client', name)
        site.clients.append(new_obj)


@AppRoute(routes=routes, url='/clients/')
class ClientListView(ListView):
    queryset = site.clients
    template_name = 'clients.html'


@AppRoute(routes=routes, url='/add-client/')
class AddClientToProductCreateView(CreateView):
    template_name = 'add_client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)

        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_client(client_name)

        product.add_client(client)


@AppRoute(routes=routes, url='/api/')
class ProductApi:
    @Debug(name='ProductApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.products).save()
