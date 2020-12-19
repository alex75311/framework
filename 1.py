# классически декоратор с параметром

def decorator_with_param(decorator_param):
    print(f"это происхолит первым еще до начала кода if __name__ == '__main__': decorator_param = {decorator_param}")
    def decorator(func):
        print(f'Это тоже до начала клиентского кода. В качестве аргумента в меня пришла декорируемая функция {func.__name__}. Это случилось когда ты написал @decorator_with_param("url=/something/") над определением функции')
        # def wrapper(*args, **kwargs):
        #     print(f'а тут запустили декорированную функцию типа {func.__name__} и она видит параметры: {decorator_param}, {args} и {kwargs}')
        #     func(*args, **kwargs)
        # return wrapper
        global a
        a = func
    return decorator

def foo(*args, **kwargs):
    print(f'я обычная функция {foo} с параметрами {args}, {kwargs}')

@decorator_with_param('url=/something/')
def foo1(*args, **kwargs):
    print(args, kwargs)
    pass


if __name__ == '__main__':
    print('начало клиентского кода')
    foo('args', kwargs='kwargs')
    print(f'а функция foo1 уже нифига не foo1, а {foo1}')
    # foo1('args', kwargs='kwargs')
    print('запускаем копию foo1')
    a('args', kwargs='kwargs')
    # decorator_with_param('url')(foo)('args', kwargs='kwargs')
