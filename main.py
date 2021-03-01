from wsgiFraimwork import Application
import views

urlpatterns = {
    '/': views.index_view,
    '/authors/': views.authors_view,
    '/contacts/': views.contact_view,
}



# пример Front controller
def secret_front(request):
    request['secret'] = 'some secret'


front_controllers = [
    secret_front
]



application = Application(urlpatterns, front_controllers)


# Запуск:
# gunicorn main:application
