from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course, ClassAttend
from course.forms import CourseForm, ClassAttendInForm
from survey.forms import SurveyForm

from user.models import Student

import datetime
# Create your views here.

# QR코드 스캐너 & 스캔후 데이터 받아서 출결 찍기
def QRScanner_in(request, pk):
    course = get_object_or_404(Course, pk=pk)
    qr_error = False    # 유효한 QR인지 확인

    if request.method == 'POST' and  'data' in request.POST and request.POST.get('data') != "":
        qr_data = request.POST.get('data')
        
        try:
            student = Student.objects.get(name=qr_data)
            # user Id값이 data에 들어감
            print("url 데이터 : " + student.name)

            # 현재 시간( 년도-월-일-시각-분)
            now = datetime.datetime.now()
            time_now = now.strftime('%H:%M:%S')
                

            context = {
                'course' : course,
                'check_time' : time_now,
                'student' : student,
                'status' : True,    # 입실 -> True, 퇴실 -> False
            }
            
            # 출석체크 페이지로 이동
            return render(request, 'attendance/attendance_check.html', context)
        except Student.DoesNotExist:
            print("유효한 QR코드가 입력값으로 들어오지 않았습니다.")
            qr_error = True # qr 에러 처리
            context = {
                'course' : course,
                'qr_error'  : qr_error, 
            }
            return render(request, 'attendance/QRScanner_in.html', context)
    context = {
        'course' : course,
        'qr_error'  : qr_error,
    }

    return render(request, 'attendance/QRScanner_in.html', context)


def QRScanner_out(request, pk):
    course = get_object_or_404(Course, pk=pk)
    qr_error = False    # 유효한 QR인지 확인

    if request.method == 'POST' and  'data' in request.POST and request.POST.get('data') != "":
        qr_data = request.POST.get('data')
        
        try:
            student = Student.objects.get(name=qr_data)
            # user Id값이 data에 들어감
            print("url 데이터 : " + student.name)

            # 현재 시간( 년도-월-일-시각-분)
            now = datetime.datetime.now()
            time_now = str(now.strftime('%Y-%m-%d %H:%M'))
                

            context = {
                'course' : course,
                'check_time' : time_now,
                'student' : student,
                'status' : False, # 입실 -> True, 퇴실 -> False
            }
            
            # 출석체크 페이지로 이동
            return render(request, 'attendance/attendance_check.html', context)
        except Student.DoesNotExist:
            print("유효한 QR코드가 입력값으로 들어오지 않았습니다.")
            qr_error = True # qr 에러 처리
            context = {
                'course' : course,
                'qr_error'  : qr_error,
            }
            return render(request, 'attendance/QRScanner_out.html', context)
    context = {
        'course' : course,
        'qr_error'  : qr_error,
    }

    return render(request, 'attendance/QRScanner_out.html', context)

# 출석 체크 모듈에 데이터 넣기
def attendance_check_in(request):
    if request.method == 'POST':
        print("post입력 확인")
        form = ClassAttendInForm(request.POST)
        if form.is_valid():
            print("form 유효성 성공")
            classAttend = form.save()
            return redirect('course:attendance_check_in_success', pk=classAttend.pk)  # 식별자(pk)를 URL에 포함시켜 리디렉션
        else:
            errors = form.errors.as_text()
            print(errors)  # 에러 메시지 출력 또는 원하는 동작 수행
            return render(request, 'attendance/attendance_error.html', {'form': form})
    else:
        return render(request, 'attendance/attendance_error.html')

# 출석 성공 페이지
def attendance_check_in_success(request, pk):
    classAttend = ClassAttend.objects.get(pk=pk)  # 식별자(pk)를 사용하여 클래스 인스턴스 조회
    course = classAttend.course_id
    student = classAttend.student_id

    context =  {'classAttend': classAttend, 'course': course, 'student': student}
    return render(request, 'attendance/attendance_check_in_success.html', context)

def attendance_check_out(request, pk):
    if request.method == 'POST':
        form = ClassAttendInForm(request.POST)
        if form.is_valid():
            form.save()
            return render('attendance/attendance_check_out.html')
    else:
       return render(request, 'attendance/attendance_error.html')

# 강좌 리스트
def course_list(request):
    course = Course.objects.all()
    
    context = {'course': course}
    return render(request, 'course/course_list.html', context)


# 강좌 추가
def create_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        survey_form = SurveyForm(request.POST)
        
        if course_form.is_valid() and survey_form.is_valid():
            course_form.save()
            survey_form.save()
            return redirect('course:course_list')  # 적절한 URL로 리다이렉트


    else:
        course_form = CourseForm()
        survey_form = SurveyForm()

    context = {
        'course_form': course_form,
        'survey_form': survey_form,
    }
    return render(request, 'course/create_course.html', context)


# 강좌 상세 페이지
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {'course': course}
    return render(request, 'course/course_detail.html', context)


# 강좌 수정
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course:course_detail', pk=course.pk)
        
    else:
        form = CourseForm(instance=course)
    context = {'form': form, 'course':course}
    return render(request, 'course/edit_course.html', context)


# 강좌 삭제
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')  # Replace 'home' with the appropriate URL name
    
    context = {'course': course}
    return render(request, 'course/delete_course.html', context)
