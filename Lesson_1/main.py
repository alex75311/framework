from ketty import Application, DebugApplication, MockApplication
from views import main_view, create_course, create_category, copy_course, \
                  category_list, student_list, student_create, add_student_by_course
from random import randint

urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
    '/copy-course/': copy_course,
    '/category-list/': category_list,
    '/student-list/': student_list,
    '/create-student/': student_create,
    '/add-student/': add_student_by_course,
}


def cookie_controller(request):
    request['cookie'] = randint(0, 99999)


front_controller = [
    cookie_controller,
]

application = Application(urlpatterns, front_controller)
