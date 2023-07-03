from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from course.forms import CourseForm, ClassAttendInForm
from survey.forms import SurveyForm

from course.models import Course, ClassAttend
from user.models import Division
from user.models import Student
from survey.models import SurveyReply,Survey
from django.db.models import Q

from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime
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
            now = datetime.now()
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
            now = datetime.now()
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

### 입실,퇴실 체크 모듈에 데이터 넣기

#입실용
def attendance_check_in(request):
    if request.method == 'POST':
        print("post입력 확인")
        form = ClassAttendInForm(request.POST)
        class_attend = form.save(commit=False)
        # 데이터 조회
        attend_data = ClassAttend.objects.filter(Q(course_id=class_attend.course_id) & Q(student_id=class_attend.student_id))
        
        if len(attend_data) == 0:
            # 데이터가 0개인 경우
            if form.is_valid():
                print("form 유효성 성공")
                classAttend = form.save()
                return redirect('course:attendance_check_in_success', pk=classAttend.pk)  # 식별자(pk)를 URL에 포함시켜 리디렉션
            else:
                errors = form.errors.as_text()
                print(errors)  # 에러 메시지 출력 또는 원하는 동작 수행
                return render(request, 'attendance/attendance_error.html', {'form': form})
        else :
            # 데이터가 1개 이상인 경우 (출입을 이미 한 경우)
            form = ClassAttendInForm(request.POST)
            course = class_attend.course_id
            student = class_attend.student_id
            context = {'course': course, 'student': student}
            return render(request, 'attendance/attendance_already_in.html', context)
    else:
        return render(request, 'attendance/attendance_error.html')

# 출석 성공 페이지
def attendance_check_in_success(request, pk):
    classAttend = ClassAttend.objects.get(pk=pk)  # 식별자(pk)를 사용하여 클래스 인스턴스 조회
    course = classAttend.course_id
    student = classAttend.student_id

    # 현재 듣고있는 강의 필드에 추가
    student.current_course_name = course.course_name
    student.save()

    context =  {
        'classAttend': classAttend, 
        'course': course, 
        'student': student
    }
    return render(request, 'attendance/attendance_check_in_success.html', context)

# 퇴실용
def attendance_check_out(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')

        end_at = request.POST.get('end_at')
        time_string = end_at
        parsed_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
        formatted_time = parsed_time.strftime("%H:%M")
        print(formatted_time)

        classAttend = ClassAttend.objects.get(Q(course_id=course_id) & Q(student_id=student_id))
        print(classAttend)

        # 설문지 제출했는지 확인
        # survey_reply = SurveyReply.objects.get(Q(course_id=course_id) & Q(student_id=student_id))
        # if survey_reply.submit_survey !=True:
        #    ...
        
        ### 퇴실 예외처리 부분
        # 강의평가를 제출했는지 확인 
        survey = Survey.objects.get(course_id=classAttend.course_id)
        try :
            survey_reply = SurveyReply.objects.get(student_id=classAttend.student_id, survey_id=survey)
            # 2차 검증
            if survey_reply.submit_survey == False:
                return render(request, 'attendance/attendance_submit_error.html', {'student' : classAttend.student_id, "course" : classAttend.course_id})
        except SurveyReply.DoesNotExist : 
            # 강의평가를 제출하지 않았으면 
            return render(request, 'attendance/attendance_submit_error.html', {'student' : classAttend.student_id, "course" : classAttend.course_id})            
        
        # classAttend.attend_state(퇴실 처리를 이미 했으면)
        if classAttend.attend_state == True :
            return render(request,'attendance/attendance_already_out.html', {'student' : classAttend.student_id, "course" : classAttend.course_id})
        
        
        classAttend.end_at = formatted_time
        classAttend.attend_state = True
        classAttend.save()
        
        course = classAttend.course_id
        student = classAttend.student_id

        # 퇴실까지 완료하면 다시 리셋
        student.current_course_name = "수강중인 강의 없음"
        student.save()

        # 건네줄 cotext
        context = {
            'course' : course,
            'student' : student,
            'classAttend' : classAttend,
        }
        return render(request,'attendance/attendance_check_out.html', context)
    else:
       return render(request, 'attendance/attendance_error.html')


# 강좌 리스트
# Create your views here.
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def course_list(request, pk):
    division = Division.objects.get(pk=pk)
    course = Course.objects.filter(division_name_id=pk)
    
    context = {
        'course': course,
        'division': division,
        
        }
    return render(request, 'course/course_list.html', context)


# 강좌 추가
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def create_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        survey_form = SurveyForm(request.POST)
        
        if course_form.is_valid() and survey_form.is_valid():
            # 코스 저장
            course = course_form.save()
            survey = survey_form.save(commit=False)
            
            survey.course_id_id = course.id
            survey_form.save()
  
            return redirect('user:division_list')  # 적절한 URL로 리다이렉트


    else:
        course_form = CourseForm()
        survey_form = SurveyForm()

    context = {
        'course_form': course_form,
        'survey_form': survey_form,
    }
    
    return render(request, 'course/create_course.html', context)


# 강좌 상세 페이지
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {'course': course}
    return render(request, 'course/course_detail.html', context)


# 강좌 수정
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
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
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')  # Replace 'home' with the appropriate URL name
    
    context = {'course': course}
    return render(request, 'course/delete_course.html', context)


# 출석 분반 선택
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def attendance_divison_list(request):
    division = Division.objects.all()

    context = {
        'division': division
    }

    return render(request, 'attendance_board/attendance_division_list.html', context)


# 출석 강의 선택
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def attendance_course_list(request, pk):
    # pk -> division_id
    course = Course.objects.filter(division_name_id=pk)

    context = {
        'course': course
    }

    return render(request, 'attendance_board/attendance_course_list.html', context)


# 강의별 출석 명단
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def attendance_course_board(request, pk):
    # pk -> course_id
    course = Course.objects.get(pk=pk)

    division = Division.objects.get(pk=course.division_name_id)
    
    students = Student.objects.filter(division_id=division.pk)
    class_attends = ClassAttend.objects.filter(Q(student_id__division_id=division.pk) & Q(course_id_id=course))

    print(f'{class_attends = }')

    context = {
        'course': course,
        'class_attends': class_attends,
        'students': students,
        'division': division,
        
    }

    return render(request, 'attendance_board/attendance_course_board.html', context)

# 출석부에서 출결 변경시 처리
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def student_attendance_update(request):
    if request.method == 'POST':
        # 폼으로 전송된 데이터 가져오기
        search_mode = request.POST.get('search_mode')
        print(search_mode)
        student_id = request.POST.get('student_id')
        print(student_id)
        course_id = request.POST.get('course_id')
        print(course_id)
        
        student = Student.objects.get(id = student_id)
        course = Course.objects.get(id = course_id)
        
        student_attend = None
        try:
            student_attend = ClassAttend.objects.get(Q(course_id=course) & Q(student_id=student))
        except:
            student_attend = ClassAttend(course_id= course, student_id=student)
            student_attend.save()
        


        print(student_attend)
        print(student_attend)
        if search_mode == "True" :
            student_attend.attend_state = True
            student_attend.save()
        elif search_mode == "False" :
            student_attend.attend_state = False
            student_attend.save()
                

        return redirect("course:attendance_course_board", pk=course.pk)
    
    student_class_attend = ClassAttend.objects
    #return redirect