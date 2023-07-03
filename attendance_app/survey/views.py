from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course
from survey.models import Survey, SurveyReply
from user.models import Division, Student
from survey.forms import SurveyReplyForm

from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
# 설분 문반 선택 리스트
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_division_list(request):
    division = Division.objects.all()
    
    context = {
        'division': division,     
        
    }
    
    return render(request, 'survey/survey_division_list.html', context)



# 설문 리스트
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_list(request, pk):
    division = Division.objects.get(pk=pk)
    course = Course.objects.filter(division_name_id=pk)
    
    
    context = {
        'division': division,
        'course': course,
        
        }
    return render(request, 'survey/survey_list.html', context)

    

# 설문 상세
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
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
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
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


# 학생 설문 페이지
@login_required
def survey_student_reply(request, pk) :
    # 해당 수강생이 현재 과목을 듣고 있는지 확인
    # 해당 학생과 surveyReply를 이어주기 위해
    student = Student.objects.get(pk=pk)
    student_course = Course.objects.get(course_name=student.current_course_name)
    
    # 해당 과목 survey
    course_survey = Survey.objects.get(course_id = student_course)
    
    context = { 
        'student_course' : student_course,
        'course_survey' : course_survey,
        'student' : student,
        
    }

    return render(request, 'survey/survey_student_reply.html', context)


# 학생 설문 제출 처리
@login_required
def survey_student_submit(request):

    if request.method == 'POST':
        form = SurveyReplyForm(request.POST)
        if form.is_valid():
            student_id = request.POST.get('student_id')
            survey_id = request.POST.get('survey_id')
            survey_reply = form.save(commit=False)

            survey_reply.student_id = Student.objects.get(id = student_id)  # 학생 ID 설정
            survey_reply.survey_id = Survey.objects.get(id = survey_id)
            survey_reply.submit_survey = True
            survey_reply.save()

            # 이 코드는 퇴실 QR까지 찍으면 
            # survey_reply.student_id.current_course_name = "수강중인 강의 없음"

            survey_reply.student_id.save()
            # 추가적인 처리 수행
            return redirect('user:show_out_qr')
        else:
            errors = form.errors.as_text()
            # 폼이 유효하지 않은 경우, 오류 처리
    else:
        form = SurveyReplyForm()
