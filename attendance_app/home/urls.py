from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('create_account', views.create_account, name='create_account')
]
