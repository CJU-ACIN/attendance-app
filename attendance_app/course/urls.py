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

    path('QRScanner_in/<int:pk>/', views.QRScanner_in, name='QRScanner_in'),
    path('QRScanner_out/<int:pk>/', views.QRScanner_out, name='QRScanner_out'),
    path('attendance_check_in', views.attendance_check_in, name='attendance_check_in'),
    path('attendance_check_in_success/<int:pk>/', views.attendance_check_in_success, name='attendance_check_in_success'),
    path('attendance_check_out/<int:pk>/', views.attendance_check_out, name='attendance_check_out'),
]
