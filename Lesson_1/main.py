import views
from ketty import Application
from random import randint

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


front_controller = [
    cookie_controller,
]

application = Application(urlpatterns, front_controller)
