from wsgiFraimwork import render


def index_view(request):
    print(request)
    secret = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret)


def authors_view(request):
    print(request)

    return '200 OK', render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
