from ketty import render


def main_view(request):
    cookie = request['cookie']
    return '200 OK', render('index.html', cookie=cookie, links=request['links'], title='Index')


def about_view(request):
    return '200 OK', render('about.html', links=request['links'], title='About')


def contact_view(request):
    return '200 OK', render('contact.html', links=request['links'], title='Contact')
