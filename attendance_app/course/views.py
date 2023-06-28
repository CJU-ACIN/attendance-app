from django.shortcuts import render

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