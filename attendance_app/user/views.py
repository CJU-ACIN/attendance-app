from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Client

# Create your views here.
def home_admin(request):
    return render(request, 'user/home_admin.html')


def login(request):
    return render(request, 'user/login.html')


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

        return redirect('user/login.html')
    else:
        return render(request, 'user/create_student_account.html')
    
    
def show_qr(request):
    return render(request, 'user/show_qr.html')