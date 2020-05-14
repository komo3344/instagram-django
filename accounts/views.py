from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
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

@login_required
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

class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.success(self.request, '암호가 변경되었습니다')
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()