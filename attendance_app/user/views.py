from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Client


# Create your views here.
# 관리자 페이지
def admin_home(request):
    return render(request, 'user/admin/admin_home.html')


# 로그인
def login(request):
    return render(request, 'user/login.html')


# 학생 계정 추가
def create_student_account(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        password = request.POST['password']
        gender = request.POST['gender']
        birthdate = request.POST['birthdate']
        division = request.POST['division']

        user = User(
            username=id,
            password=password,
            is_staff=0,
        )
        user.save()

        client = Client(
            user=user,
            name=name,
            gender=gender,
            birth_date=birthdate,
            division=division,
        )

        client.save()

        print('account created!')

        return redirect('user/student/login')
    else:
        return render(request, 'user/student/create_student_account.html')


## QR 코드 보여주기
# 입실    
def show_in_qr(request):
    return render(request, 'user/student/show_in_qr.html')


# 퇴실    
def show_out_qr(request):
    return render(request, 'user/student/show_out_qr.html')


# 관리자 목록
def admin_list(request):
    staff_user = User.objects.filter(is_staff=1)

    # staff_user에 해당하는 Client 객체들 가져오기
    teacher = Client.objects.filter(user__in=staff_user)
    
    context = {
        'teacher': teacher,
        
        }
    
    return render(request, 'user/admin/admin_list.html', context)

# 관리자 생성
def admin_create(request):
    if request.method == 'POST':

        id = request.POST['id']
        name = request.POST['name']
        password = request.POST['password']

        user = User(
            username=id,
            password=password,
            is_staff=1,
        )
        user.save()

        client = Client(
            user=user,
            name=name,
        )

        client.save()

        print('account created!')
        
        return redirect('admin_list')
    
    else:
        return render(request, 'user/admin/admin_create.html')
    

# 관리자 삭제
def admin_delete(request):
    if request.method == 'POST':

        pk = request.POST['teacher_pk']

        client = Client.objects.get(pk=pk)

        client.delete()

        print('account deleted!')
        
        return redirect('admin_list')
    
    return redirect('admin_list')