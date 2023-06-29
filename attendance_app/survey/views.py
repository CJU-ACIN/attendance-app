from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course
from survey.models import Survey, SurveyReply
from user.models import Division

# Create your views here.
# 설분 문반 선택 리스트
def survey_division_list(request):
    division = Division.objects.all()
    
    context = {
        'division': division,     
        
    }
    
    return render(request, 'survey/survey_division_list.html', context)



# 설문 리스트
def survey_list(request, pk):
    division = Division.objects.get(pk=pk)
    course = Course.objects.filter(division_name_id=pk)
    
    
    context = {
        'division': division,
        'course': course,
        
        }
    return render(request, 'survey/survey_list.html', context)

    

# 설문 상세
def survey_detail(request, pk):
    # 쿼리 변수 초기화
    survey = None
    course = None
    divison = None
    survey_reply = None
    
    # 쿼리 조회 시도
    try:
        survey = Survey.objects.get(course_id=pk)
        course = Course.objects.get(pk=survey.course_id.pk)
        division = Division.objects.get(pk=course.division_name_id)
    
    # 쿼리 조회 결과가 없을 경우 패스
    except Survey.DoesNotExist:
        pass
    
    except Course.DoesNotExist:
        pass
    
    
    # survey = get_object_or_404(Survey, course_id=pk)
    # course = get_object_or_404(Course, pk=survey.course_id.pk)
    
    if survey is not None:
        survey_reply = SurveyReply.objects.filter(survey_id = survey.pk)
    
    
    context = {
        'survey': survey,
        'course': course,
        'division': division,
        'survey_reply': survey_reply,
        
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