from ketty import Application
import views
from random import randint

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
}


def cookie_controller(request):
    request['cookie'] = randint(9999)


front_controller = [
    cookie_controller,
]

application = Application(urlpatterns, front_controller)
