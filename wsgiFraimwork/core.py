import quopri
from wsgiref.util import setup_testing_defaults


class Application:
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
        value_decode_str = quopri.decodestring(value_b)
        return value_decode_str.decode('UTF-8')

    def add_route(self, url):
        # паттерн декоратор
        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns, front_controllers):
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {'method': method, 'data': data,
                       'request_params': request_params}
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)
            code, body = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [body.encode('utf-8')]
        else:
            # Если url нет в urlpatterns - то страница не найдена
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Eror 404 : Not Found ']


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
