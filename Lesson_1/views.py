from ketty import render
from models import TrainingSite
from logging_mod import Logger

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log(f'Список курсов: {site.courses}')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    categories = site.categories
    if request['method'] == 'POST':
        data = request['params_post']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
    return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    categories = site.categories
    if request['method'] == 'POST':
        data = request['params_post']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
    return '200 OK', render('create_category.html', categories=categories)


def copy_course(request):
    request_params = request['params_get']
    print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


def student_list(request):
    return '200 OK', render('student_list.html', objects_list=site.students)


def student_create(request):
    data = request['params_post']
    if data:
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
    return '200 OK', render('create_student.html')


def add_student_by_course(request):
    data = request['params_post']
    if data:
        add_student = data['student_name']
        add_course = data['course_name']
        student = site.get_student(add_student)
        course = site.get_course(add_course)
        student.courses.append(course)

    students = site.students
    courses = site.courses
    return '200 OK', render('add_student.html', students=students, courses=courses)
