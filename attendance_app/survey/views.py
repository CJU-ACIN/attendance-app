from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course
from survey.models import Survey, SurveyReply

# Create your views here.
# 설문 리스트
def survey_list(request):
    course = Course.objects.all()
    survey = Survey.objects.all()
    
    context = {
        'course': course,
        'survey': survey,
        
        }
    return render(request, 'survey/survey_list.html', context)

    

# 설문 상세
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, course_id=pk)
    course = get_object_or_404(Course, pk=survey.course_id.pk)
    
    survey_reply = SurveyReply.objects.filter(survey_id = survey.pk)
    
    context = {
        'survey': survey,
        'course': course,
        'survey_reply': survey_reply
        }
    
    return render(request, 'survey/survey_detail.html', context)


# 설문 상세
def survey_reply_detail(request, pk):
    survey_reply = get_object_or_404(SurveyReply, pk=pk)
    survey = get_object_or_404(Survey, pk=survey_reply.survey_id.pk)
    course = get_object_or_404(Course, pk=survey.course_id.pk)
    
    context = {
        'survey_reply': survey_reply,
        'survey': survey,
        'course': course,
        }
    
    return render(request, 'survey/survey_reply_detail.html', context)