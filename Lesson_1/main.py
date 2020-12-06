from ketty import Application
import views
from random import randint

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


def link_controller(request):
    request['links'] = ''
    for title in urlpatterns.keys():
        request['links'] += f'<br><a href={title}>{title}</a>'
    print(request)


front_controller = [
    cookie_controller,
    link_controller,
]

application = Application(urlpatterns, front_controller)
