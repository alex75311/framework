from ketty import render


def main_view(request):
    cookie = request['cookie']
    return '200 OK', render('index.html', cookie=cookie)


def about_view(request):
    return '200 OK', render('about.html')