from django.contrib import admin
from django.urls import path
from .views import GetComments, GetPhones,get_comments_page,HomePage,get_all_phone_numbers,GetNegativeComments,get_negative_comments

urlpatterns = [

    path('api/comments/', GetComments.as_view(), name='comments'),#api для парсинга коментариев
    path('api/phones/',GetPhones.as_view()),#api для получения номеров телефонов
    path('get-comments/', get_comments_page, name='get_comments_page'),#страница для парсинга 
    path('get-phones/',get_all_phone_numbers,name='phones'),#страница для получения номеров телефонов
    path('', HomePage.as_view(), name='home'),#главная страница
    path('api/negative/', GetNegativeComments.as_view(), name='negativeapi'),#api для получения комментариев с негативной тональностью
    path('negative_comments', get_negative_comments, name='negative'),#страница с негативными коментариями

    ]