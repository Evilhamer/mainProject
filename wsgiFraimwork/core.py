class Application:
    def __init__(self, urlpatterns, front_controllers):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        # Текущий URL
        path = environ['PATH_INFO']

        # add /
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            # получение viev по url
            view = self.urlpatterns[path]
            request = {}

            # добавляем параметры запросов(метод и данные)

            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            # добавляем в запрос данные из front controllers

            for controller in self.front_controllers:
                controller(request)
            # вызываем view, получаем результат
            code, body = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [body.encode('utf-8')]

        else:
            # Если url нет в urlpatterns - то страница не найдена
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Eror 404 : Not Found ']

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
