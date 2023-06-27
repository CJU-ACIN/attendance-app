from django.urls import path, include
from course import views

from django.contrib.auth import views as auth_views

app_name = 'course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    # path('create/', views.create_course, name='create_course'),
    # path('edit/', views.edit_course, name='edit_course'),
    # path('delete/', views.delete_course, name='delete_course'),
]
