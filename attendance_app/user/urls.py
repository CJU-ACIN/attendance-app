# user.urls

from django.urls import path
from user import views


urlpatterns = [
    path('', views.home_admin, name='home_admin'),
    path('login/', views.login, name='login'),
    path('create_student_account/', views.create_student_account, name='create_student_account'),
    path('show_qr', views.show_qr, name='show_qr')
]
