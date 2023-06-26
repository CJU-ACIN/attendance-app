# user.urls

from django.urls import path

from user import views


urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_list', views.admin_list, name='admin_list'),
    path('admin_create', views.admin_create, name='admin_create'),
    path('admin_delete', views.admin_delete, name='admin_delete'),
    
    path('login/', views.login, name='login'),
    path('create_student_account/', views.create_student_account, name='create_student_account'),
    
    path('show_in_qr', views.show_in_qr, name='show_in_qr'),
    path('show_out_qr', views.show_out_qr, name='show_out_qr'),
]
