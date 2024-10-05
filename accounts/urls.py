from django.urls import path, include
from .views import login_view,logout_view


urlpatterns = [
    
    path('api/auth/', include('djoser.urls')),#эндпоинты джозера 
    path('api/auth/', include('djoser.urls.jwt')),#эндпоинты джозера 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]