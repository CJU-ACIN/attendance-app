# user.urls

from django.urls import path

from user import views


urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),


    path('signup/', views.signup, name='signup'),
    
    path('show_in_qr', views.show_in_qr, name='show_in_qr'),
    path('show_out_qr', views.show_out_qr, name='show_out_qr'),
]
