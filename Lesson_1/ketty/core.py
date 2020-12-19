import urllib


class Application:

    def add_route(self, url):
        def inner(view):
            self.urlpatterns[url] = view
        return inner

    def parse_input_params(self, data: str):
        """Парсинг параметров (GET или POST)"""
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                key, value = param.split('=')
                result[key] = value
        return result

    def get_input_data(self, env: dict):
        """Получение параметров POST"""
        result = {}
        length = env.get('CONTENT_LENGTH')
        if length:
            result = env['wsgi.input'].read(int(length)).decode('utf-8')
            result = urllib.parse.unquote(result)
        return result

    def __init__(self, urlpatterns: dict, front_controllers: list):
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']

        method = env['REQUEST_METHOD']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.urlpatterns:
            # получаем view по url
            view = self.urlpatterns[path]
            request = {}

            # добавляем метод которым пришел запрос
            request['method'] = method

            # Получаем пришедшие параметры
            request['params_get'] = self.parse_input_params(env['QUERY_STRING'])
            params_str = self.get_input_data(env)
            request['params_post'] = self.parse_input_params(params_str)
            print(request['params_get'], request['params_post'])

            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)
            # получаем из view код и страницу
            code, text = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Not Found']


class DebugApplication(Application):
    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super(DebugApplication, self).__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response, *args, **kwargs):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class MockApplication(Application):
    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super(MockApplication, self).__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response, *args, **kwargs):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Mock']
