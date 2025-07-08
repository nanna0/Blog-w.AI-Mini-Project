from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, CustomAuthenticationForm


# 회원가입
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "account/sign_up.html", {"form": form})


# 로그인
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("post_list")
    else:
        form = CustomAuthenticationForm()
    return render(request, "account/login.html", {"form": form})


# 로그아웃
@login_required  # 로그인한 사용자만 접근 가능
def logout_view(request):
    logout(request)
    return redirect("post_list")
