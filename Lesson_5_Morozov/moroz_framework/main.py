from quopri import decodestring
from os import path

from requests import GetRequests, PostRequests
from components.content_types import CONTENT_TYPES_MAP


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page not Fоund'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].lower()  # не уверен, что это хорошо ;-)

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'POST-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'GET-параметры: {Framework.decode_value(request_params)}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path.startswith(self.settings.STATIC_URL):
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(self.settings.STATIC_ROOT, file_path)
        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        start_response(code, [('Content-Type', content_type)])
        return [body]

    @staticmethod
    def decode_value(data):
        decoded_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            val_decode_str = decodestring(val).decode('utf-8')
            decoded_data[k] = val_decode_str
        return decoded_data

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        file_extension = path.splitext(file_name)[1]
        return content_types_map.get(file_extension, 'text/html')

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content
