from django.urls import path, include
from course import views

from django.contrib.auth import views as auth_views

app_name = 'course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('detail/<int:pk>/', views.course_detail, name='course_detail'),
    
    path('create/', views.create_course, name='create_course'),
    path('edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'),
]
