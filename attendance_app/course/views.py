from django.shortcuts import render, redirect


# Create your views here.
def course_list(request):
    
    context = {}
    return render(request, 'course/course_list.html', context)