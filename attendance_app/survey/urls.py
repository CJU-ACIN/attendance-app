from django.urls import path, include
from survey import views


app_name = 'survey'

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    # path('detail/<int:pk>/', views.course_detail, name='course_detail'),
    
    # path('create/', views.create_course, name='create_course'),
    # path('edit/<int:pk>/', views.edit_course, name='edit_course'),
    # path('delete/<int:pk>/', views.delete_course, name='delete_course'),
]
