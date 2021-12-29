from moroz_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html',
                                main_menu=request.get('main_menu', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html',
                                main_menu=request.get('main_menu', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html',
                                main_menu=request.get('main_menu', None))
