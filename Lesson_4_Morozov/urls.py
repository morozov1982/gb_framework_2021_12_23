from views import Index, About, Contacts, ProductsList, CreateProduct, \
    CategoryList, CreateCategory, CopyProduct


def main_menu_front(request):
    request['main_menu'] = {
        'Главная': '/',
        'О нас': '/about/',
        'Товары': '/categories/',
        'Контакты': '/contacts/',
    }


fronts = [main_menu_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/products/': ProductsList(),
    '/create-product/': CreateProduct(),
    '/categories/': CategoryList(),
    '/create-category/': CreateCategory(),
    '/copy-product/': CopyProduct(),
}
