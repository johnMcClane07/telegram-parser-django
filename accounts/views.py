from django.shortcuts import render, redirect
from rest_framework import status
import requests


def login_view(request):
    """
    View-функция для страницы логина.

    Если запрос был GET, то просто отображается страница логина.
    Если запрос был POST, то на сервер будет отправлен запрос на создание токена
    и, если ответ будет успешным, то токены будут сохранены в сессии, а пользователь
    будет перенаправлен на домашнюю страницу. Если ответ будет неудачным, то
    страница логина будет отображена снова, но с сообщением об ошибке.
    """
    if request.method == 'POST':
        print(request.POST)
        response = requests.post('http://localhost:8000/api/auth/jwt/create/', data=request.POST)
        if response.status_code == status.HTTP_200_OK:
            tokens = response.json()
            print(tokens)
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            return redirect('home')
        else:
            print(response.json())
            return render(request, 'login.html', {'error': response.json().get('detail')})

    return render(request, 'login.html')

def logout_view(request):
    """
    View-функция для страницы выхода из аккаунта.

    Если запрос был POST, то токены будут удалены из сессии, а пользователь
    будет перенаправлен на домашнюю страницу.
    """
    if request.method == 'POST':
        del request.session['access_token']
        del request.session['refresh_token']
        return redirect('home')