from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Student

from django.contrib.auth import login, authenticate

from user.forms import SignUpForm, ClientForm
from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



# Create your views here.
# 관리자 페이지
def admin_home(request):
    return render(request, 'user/admin/admin_home.html')


# 학생 계정 추가
def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        client_form = ClientForm(request.POST)
        
        if signup_form.is_valid() and client_form.is_valid():
            # 회원가입 후 자동 로그인
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password')
            
            # 비밀번호 유효성 검사
            try:
                validate_password(password)
            except ValidationError as validation_error:
                messages.error(request, f"{validation_error}")
                return render(request, 'user/student/signup.html', {'signup_form': signup_form, 'client_form': client_form})
            
            user = signup_form.save()
            student = client_form.save(commit=False)
            student.user = user
            student.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'home/home.html')

    else:
        signup_form = SignUpForm()
        client_form = ClientForm()

    return render(request, 'user/student/signup.html', {'signup_form': signup_form, 'client_form': client_form})


## QR 코드 보여주기
# 입실    
def show_in_qr(request):
    return render(request, 'user/student/show_in_qr.html')


# 퇴실    
def show_out_qr(request):
    return render(request, 'user/student/show_out_qr.html')


    
