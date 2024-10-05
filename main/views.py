from rest_framework.views import APIView
from .parser import get_post_comments
from rest_framework.response import Response
from rest_framework import status
import asyncio
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
import requests
from rest_framework.permissions import IsAuthenticated
from history.views import  make_request, RefreshTokenExpiredException
from .models import Comment
from history.serializers import CommentSerializer
from .serializers import CommentSerializer
from rest_framework import filters
from rest_framework import generics
from django.http import HttpResponse
import pandas as pd




class GetComments(APIView):
    """
    API для получения комментариев из поста.

    Получает URL поста в теле запроса, парсит комментарии к этому посту
    и возвращает их.

    """
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        post_url = request.data.get('url')
        try:
            comments = asyncio.run(get_post_comments(post_url)) 
            if isinstance(comments, str) and comments.startswith('Error'):
                return Response({'error': comments}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(comments, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPhones(generics.ListAPIView):
    """
    API для получения всех номеров телефонов из комментариев.

    Возвращает список комментариев, которые содержат номер телефона,
    с подробной информацией о посте, к которому относится комментарий.

    """
    permission_classes=[IsAuthenticated]
    queryset = Comment.objects.filter(sender_phone__isnull=False).select_related('post')
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['post__company', 'post__link']
    
class GetNegativeComments(generics.ListAPIView):
    """
    API для получения всех негативных комментариев.

    Возвращает список комментариев, которые имеют негативный окрас,
    с подробной информацией о посте, к которому относится комментарий.

    """
    permission_classes=[IsAuthenticated]
    queryset = Comment.objects.filter(polarity='negative').select_related('post')
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['post__company', 'post__link']
    
         

class HomePage(TemplateView):
    template_name = 'home.html'


def get_comments_page(request):

    """
    View-функция для отображения комментариев к посту, полученных в результате парсинга 

    Если запрос был POST, то делается запрос к API на получение комментариев,
    и если ответ был успешным, то отображается страница с комментариями.
    Если ответ был неудачным, то отображается страница с ошибкой.
    Если токен доступа истек, то перенаправляется на страницу входа.
    Если возникла ошибка при отправке запроса, то отображается страница с ошибкой.
    
    Если запрос был GET, то отображается страница для ввода url.
    """
    if request.method == 'POST':
        post_url = request.POST.get('url')     
        api_url = 'http://localhost:8000/api/comments/' 
        
        try:
            response = make_request(request, api_url, method='POST', data={'url': post_url})
            if response.status_code == 200:
                comments = response.json() 
                return render(request, 'comments.html', {'comments': comments})
            else:
                error_message = response.json().get('error', 'Ошибка при получении комментариев.')
                return render(request, 'comments.html', {'error': error_message})
        except RefreshTokenExpiredException:
            return redirect('login')
        except requests.exceptions.RequestException as e:
            return render(request, 'comments.html', {'error': str(e)})

    return render(request, 'url.html')


def get_all_phone_numbers(request):
    print(request.GET)
    """
    View-функция для отображения всех номеров телефонов из комментариев.

    Если в GET-запросе передан параметр 'search', то делается запрос к API на получение
    номеров телефонов по этому параметру.
    Если параметр 'search' не передан, то делается запрос к API на получение всех номеров
    телефонов.
    Если ответ от API был успешным, то отображается страница с номерами телефонов.
    Если ответ от API был неудачным, то отображается страница с ошибкой.
    Если токен доступа истек, то перенаправляется на страницу входа.
    Если возникла ошибка при отправке запроса, то отображается страница с ошибкой.
    """
    search_by = request.GET.get('search')
    if search_by:
        api_url=f'http://localhost:8000/api/phones/?search={search_by}'
    else:
        api_url='http://localhost:8000/api/phones/'
    try:
        response = make_request(request, api_url, method='GET')
        if response.status_code == 200:
            phone_numbers = response.json()
            if request.GET.get('download') == 'excel':
                df = pd.DataFrame(phone_numbers)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="phone_numbers.xlsx"'
                df.to_excel(response, index=False)
                return response 
            return render(request, 'phones.html', {'phone_numbers': phone_numbers})
        else:
            error_message = response.json().get('error', 'Ошибка при получении комментариев.')
            return render(request, 'phones.html', {'error': error_message})
    except RefreshTokenExpiredException:
            return redirect('login')
    except requests.exceptions.RequestException as e:
            return render(request, 'phones.html', {'error': str(e)})    


def get_negative_comments(request):
    """
    View-функция для отображения комментариев с негативной тональностью.

    Если в GET-запросе передан параметр 'search', то делается запрос к API на получение
    комментариев с негативной тональностью по этому параметру.
    Если параметр 'search' не передан, то делается запрос к API на получение всех комментариев
    с негативной тональностью.
    Если ответ от API был успешным, то отображается страница с комментариями.
    Если ответ от API был неудачным, то отображается страница с ошибкой.
    Если токен доступа истек, то перенаправляется на страницу входа.
    Если возникла ошибка при отправке запроса, то отображается страница с ошибкой.
    """
    search_by = request.GET.get('search')
    if search_by:
        api_url=f'http://localhost:8000/api/negative/?search={search_by}'
    else:
        api_url='http://localhost:8000/api/negative/'
    try:
        response = make_request(request, api_url, method='GET')
        if response.status_code == 200:
            negative_comments = response.json() 
            print(negative_comments)
            if request.GET.get('download') == 'excel':
                df = pd.DataFrame(negative_comments)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="negative_comments.xlsx"'
                df.to_excel(response, index=False)
                return response 
            return render(request, 'negative.html', {'negative_comments': negative_comments})
        else:
            error_message = response.json().get('error', 'Ошибка при получении комментариев.')
            return render(request, 'negative.html', {'error': error_message})
    except RefreshTokenExpiredException:
            return redirect('login')
    except requests.exceptions.RequestException as e:
            return render(request, 'negative.html', {'error': str(e)})






        


