class Application:
    def parse_input_params(self, data: str):
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                key, value = param.split('=')
                result[key] = value
        return result

    def get_input_data(self, env):
        length = env['CONTENT_LENGTH']
        if length:
            result = env['wsgi.input'].read(int(length)).decode('utf-8')
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
            if method == 'GET':
                request['params'] = self.parse_input_params(env['QUERY_STRING'])
            elif method == 'POST':
                params_str = self.get_input_data(env)
                request['params'] = self.parse_input_params(params_str)

            print('', request['params'])
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
