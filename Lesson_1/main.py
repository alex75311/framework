import views
from ketty import Application
from random import randint

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact_view,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


def link_controller(request):
    request['links'] = []
    for title in urlpatterns.keys():
        request['links'].append(title)


front_controller = [
    cookie_controller,
    link_controller,
]

application = Application(urlpatterns, front_controller)
