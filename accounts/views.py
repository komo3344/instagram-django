from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 되었습니다.')
            next_url = request.GET.get('next', 'root')
            return redirect(next_url)
    else:
        form = forms.SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })