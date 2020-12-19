from ketty import Application, DebugApplication, MockApplication
from views import main_view, create_course, create_category, copy_course, category_list
from random import randint

urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
    '/copy-course/': copy_course,
    '/category-list/': category_list,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


front_controller = [
    cookie_controller,
]

application = Application(urlpatterns, front_controller)
