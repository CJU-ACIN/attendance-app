from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course
from course.forms import CourseForm, ClassAttendForm
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
            time_now = now.now
                

            context = {
                'course' : course,
                'check_time' : time_now,
                'student' : student,
                'status' : True,    # 입실 -> True, 퇴실 -> False
            }
            
            # 출석체크 페이지로 이동
            return render(request, 'course/attendance_check.html', context)
        except Student.DoesNotExist:
            print("유효한 QR코드가 입력값으로 들어오지 않았습니다.")
            qr_error = True # qr 에러 처리
            context = {
                'course' : course,
                'qr_error'  : qr_error, 
            }
            return render(request, 'course/QRScanner_in.html', context)
    context = {
        'course' : course,
        'qr_error'  : qr_error,
    }

    return render(request, 'course/QRScanner_in.html', context)


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
            return render(request, 'course/attendance_check.html', context)
        except Student.DoesNotExist:
            print("유효한 QR코드가 입력값으로 들어오지 않았습니다.")
            qr_error = True # qr 에러 처리
            context = {
                'course' : course,
                'qr_error'  : qr_error,
            }
            return render(request, 'course/QRScanner_out.html', context)
    context = {
        'course' : course,
        'qr_error'  : qr_error,
    }

    return render(request, 'course/QRScanner_out.html', context)

# 출석 체크 하기
def attendance_check(request):
    if request.method == 'POST':
        form = ClassAttendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success-page')
    else:
        return render(request, 'add_classattend.html')

# 강좌 리스트
def course_list(request):
    course = Course.objects.all()
    
    context = {'course': course}
    return render(request, 'course/course_list.html', context)


# 강좌 추가
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course:course_list')  # 적절한 URL로 리다이렉트

    else:
        form = CourseForm()

    return render(request, 'course/create_course.html', {'form': form})


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
