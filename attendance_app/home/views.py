from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def login_page(request):
    return render(request, 'home/login.html')


def create_account(request):
    if request.method == 'POST':
        ...
    else:
        return render(request, 'home/create_account.html')