from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            messages.success(request, '회원가입이 되었습니다.')
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = forms.SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })