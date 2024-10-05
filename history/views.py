from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from main.models import Post
from .serializers import PostRetrieveSerializer, PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
import requests
from django.db.models import Count, Case, When
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


class RefreshTokenExpiredException(Exception):
    """Исключение, которое выбрасывается, когда Refresh токен истек"""
    pass    


class HistoryView(ModelViewSet):
    """
    API для работы с историей постов.
    Позволяют получать список постов, а также отдельные посты.
    """
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    http_method_names = ['get', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['company', 'link']
    permission_classes=[IsAuthenticated]


    def retrieve(self,request,pk=None):
        """
        Возвращает статистику поста: количество позитивных, негативных и
        нейтральных комментариев, а также количество комментариев и номеров
        телефонов.
        """
        post = get_object_or_404(
            Post.objects.annotate(
                positive=Count(
                    Case(When(comments__polarity='positive', then=1))
                ),
                negative=Count(
                    Case(When(comments__polarity='negative', then=1))
                ),
                neutral=Count(
                    Case(When(comments__polarity='neutral', then=1))
                ),
                length=Count('comments'),
                phones=Count(
                    Case(When(comments__sender_phone__isnull=False, then=1))
                ),
            ),
            pk=pk,
        )
        serializer = PostRetrieveSerializer(post)
        return Response(serializer.data)



def make_request(request, api_url, method='GET', **kwargs):
    
    """
    Делает запрос к API, используя токен доступа, полученный при аутентификации.
    Если токен доступа истек, пытается получить новый токен и повторяет запрос.
    """
    
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.request(method, api_url, headers=headers, **kwargs)

    if response.status_code == 401:
        new_access_token = get_access_token(request)
        if isinstance(new_access_token, HttpResponse):
            raise RefreshTokenExpiredException

        new_headers = headers.copy()
        new_headers['Authorization'] = f'Bearer {new_access_token[0]["access_token"]}'

        response = requests.request(method, api_url, headers=new_headers, **kwargs)

    return response


def get_access_token(request):
    """
    Обновляет токен доступа, если он истек.
    
    :param request: запрос, из которого извлекается токен доступа
    :return: ответ, содержащий обновленный токен доступа
    :raises: Redirect на страницу входа, если токен истек
    """
    
    refresh_token = request.session.get('refresh_token')

    if not refresh_token:
        return redirect('login')

    response = requests.post('http://localhost:8000/api/auth/jwt/refresh/', data={'refresh': refresh_token})
    if response.status_code == 401:
        return redirect('login')
    if response.status_code == 200:
        new_access_token = response.json().get('access')
        if new_access_token:
            request.session['access_token'] = new_access_token
            return {'access_token': new_access_token}, 200
    return {'error': 'Unable to refresh token'}, response.status_code

    
def history(request):
    """
    История запросов.

    Получает из API историю запросов.
    Если запрос содержит параметр search, то делает поиск по истории.
    Если токен доступа истек, то пытается его обновить и повторяет запрос.
    Если обновить токен невозможно, то перенаправляет на страницу входа.
    Если возникла ошибка при получении истории, то отображает ошибку.
    """
    serach_by = request.GET.get('search')
    if serach_by:
        api_url = f'http://localhost:8000/api/posts/?search={serach_by}'
    else:
        api_url = 'http://localhost:8000/api/posts/'
    if request.method == 'GET':    
        try:
            response=make_request(request, api_url, method='GET')

            if response.status_code == 200:
                posts=response.json()
                return render(request, 'history.html', {'posts': posts})
            else:
                error_message = response.json().get('error', 'Ошибка при получении комментариев.')
                return render(request, 'history.html', {'error': error_message})
        except RefreshTokenExpiredException:
            return redirect('login')
        except requests.exceptions.RequestException as e:
            return render(request, 'history.html', {'error': str(e)})

    return render(request, 'url.html')
def post_detail(request, post_id):
    """
    View-функция для отображения деталей поста.

    Если запрос был GET, то делается запрос к API на получение деталей поста,
    и если ответ был успешным, то отображается страница с деталями поста.
    Если ответ был неудачным, то отображается страница с ошибкой.
    Если токен доступа истек, то перенаправляется на страницу входа.
    Если возникла ошибка при отправке запроса, то отображается страница с ошибкой.
    
    Если запрос был POST, то делается запрос к API на удаление поста,
    и если ответ был успешным, то перенаправляется на страницу истории.
    Если ответ был неудачным, то отображается страница с ошибкой.
    Если токен доступа истек, то перенаправляется на страницу входа.
    Если возникла ошибка при отправке запроса, то отображается страница с ошибкой.
    """

    api_url = f'http://localhost:8000/api/posts/{post_id}/'
    if request.method == 'GET':
        
        try:
            response = make_request(request, api_url, method='GET')
            if response.status_code == 200:
                post = response.json()
                return render(request, 'post_detail.html', {'post': post})
            else:
                error_message = response.json().get('error', 'Ошибка при получении деталей поста.')
                return render(request, 'post_detail.html', {'error': error_message})
        except RefreshTokenExpiredException:
            return redirect('login')
        except requests.exceptions.RequestException as e:
            return render(request, 'post_detail.html', {'error': str(e)})
        

    elif request.method == 'POST' :
        try:
            response = make_request(request, api_url, method='DELETE')
            if response.status_code == 204:  
                return redirect('history')
            else:
                error_message = response.json().get('error', 'Ошибка при удалении поста.')
                return render(request, 'post_detail.html', {'error': error_message})
        except RefreshTokenExpiredException:  
            return redirect('login')
        except requests.exceptions.RequestException as e:
            return render(request, 'post_detail.html', {'error': str(e)})


    return render(request, 'url.html')



    

    
    


