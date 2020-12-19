from ketty import Application
import views
from random import randint

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


def link_controller(request):
    request['links'] = ''
    for title in urlpatterns.keys():
        request['links'] += f'<br><a href={title}>{title}</a>'


front_controller = [
    cookie_controller,
]

application = Application(urlpatterns, front_controller)
