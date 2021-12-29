from views import Index, About, Contacts


def main_menu_front(request):
    request['main_menu'] = {
        'index': '/',
        'about': '/about/',
        'contacts': '/contacts/',
    }


fronts = [main_menu_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
}
