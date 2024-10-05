from django.urls import path, include
from .views import HistoryView,history,post_detail
from rest_framework.routers import DefaultRouter

#роутер для api истории запросов 
router = DefaultRouter()
router.register('api/posts', HistoryView, basename='post')

urlpatterns = [
    path('', include(router.urls)), 
    path('history/',history,name='history'),#история запросов
    path('history/<int:post_id>/', post_detail, name='post_detail'),#информация о посте 
]
