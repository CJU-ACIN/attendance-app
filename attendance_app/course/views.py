from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from course.models import Course
from course.forms import CourseForm

import datetime
# Create your views here.

# QR코드 스캐너 & 스캔후 데이터 받아서 출결 찍기
def QRScanner_in(request):

    subject_name = '인공지능'
    teacher = '서강산'
    class_time = '3~6'
    if request.method == 'POST' and  'data' in request.POST and request.POST.get('data') != "":
        data = request.POST.get('data')

        # user Id값이 data에 들어감
        print("url 데이터 : " + data)

        # 현재 시간( 년도-월-일-시각-분)
        now = datetime.datetime.now()
        time_now = str(now.strftime('%Y-%m-%d %H:%M'))
        

        context = {
            'qr_data' : data,
            'check_time' : time_now,
            'subject_name' : subject_name,
            'teacher' : teacher,
            'status' : True,
        }
        
        return render(request, 'course/attendance_check.html', context)

    context = {
        'subject_name' : subject_name,
        'teacher' : teacher,
        'class_time' : class_time
    }

    return render(request, 'course/QRScanner_in.html', context)


def QRScanner_out(request):
    subject_name = '인공지능'
    teacher = '서강산'
    class_time = '3~6'
    if request.method == 'POST' and  'data' in request.POST and request.POST.get('data') != "":
        data = request.POST.get('data')

        # user Id값이 data에 들어감
        print("url 데이터 : " + data)

        # 현재 시간( 년도-월-일-시각-분)
        now = datetime.datetime.now()
        time_now = str(now.strftime('%Y-%m-%d %H:%M'))
        

        context = {
            'qr_data' : data,
            'check_time' : time_now,
            'subject_name' : subject_name,
            'teacher' : teacher,
            'status' : False,
        }
        
        return render(request, 'course/attendance_check.html', context)

    context = {
        'subject_name' : subject_name,
        'teacher' : teacher,
        'class_time' : class_time
    }

    return render(request, 'course/QRScanner_out.html', context)
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
