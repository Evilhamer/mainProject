

from wsgiFraimwork import render
from wsgiFraimwork import Application


# from wsgiFraimwork import render
# import quopri
# import json


def main_view(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    # Просто возвращаем текст
    return '200 OK', "About"


def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение! Отправитель - {Application.decode_value(email)}, '
              f'тема - {Application.decode_value(title)}, текст - '
              f' {Application.decode_value(text)}.')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')









# def index_view(request):
#     print(request)
#     secret = request.get('secret_key', None)
#     return '200 OK', render('index.html', secret=secret)
#
#
# def authors_view(request):
#     print(request)
#
#     return '200 OK', render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
#
#
# def contact_view(request):
#     # Проверка метода запроса
#     if request['method'] == 'POST':
#         print(request)
#         data = request['data']
#         title = data['title']
#         text = data['text']
#         email = data['email']
#         log_msg(data)
#         print(f'Нам пришло сообщение от {email} с темой {decode_value(title)} и текстом {decode_value(text)}')
#         return '200 OK', render('contact.html')
#     else:
#         return '200 OK', render('contact.html')
#
#
# def log_msg(data):
#
#     with open('./data/data.json', 'a') as f:
#         json.dump(data, f, sort_keys=True, indent=4)
#
# def decode_value(val):
#     val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
#     val_decode_str = quopri.decodestring(val_b)
#     return val_decode_str.decode('UTF-8')
