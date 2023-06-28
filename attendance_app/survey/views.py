from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course


# Create your views here.
def survey_list(request):
    course = Course.objects.all()
    
    context = {'course': course}
    return render(request, 'survey/survey_list.html', context)