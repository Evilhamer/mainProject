from wsgiFraimwork import Application
import views

routes = {
    '/': views.index_view,
    '/a/': views.authors_view,
}


# Front controller
def secret_front(request):
    request['secret'] = 'some secret'


fronts = [
    secret_front
]


application = Application(routes, fronts)

# Запуск:
# gunicorn main:application