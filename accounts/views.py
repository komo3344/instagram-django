from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib import messages
from . import forms

login = LoginView.as_view(template_name="accounts/login_form.html")

def logout(request):
    messages.success(request, '로그아웃 되었습니다')
    return logout_then_login(request)

def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            messages.success(request, '회원가입이 되었습니다.')
            auth_login(request, signed_user)
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = forms.SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })

def profile_edit(request):
    if request.method == 'POST':
        form = forms.ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정/저장 되었습니다.')
            return redirect('profile_edit')
    else:
        form = forms.ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit_form.html',{
        'form': form
    })