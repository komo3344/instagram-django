from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm)
from .models import User

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.fields.get('email').required = True
        self.fields.get('first_name').required = True
        self.fields.get('last_name').required = True
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if email:
            if qs.exists():
                raise forms.ValidationError('이미 등록된 이메일 주소 입니다.')
        return email
        
    class Meta(UserCreationForm.Meta):
            model = User
            fields = ['username', 'first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'website_url', 'bio', 'gender', 'phone_number']

class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data["old_password"]
        new_password2 = self.cleaned_data["new_password2"]
        # new_password2 = super().clean_new_password2() 상속받은 것을 사용하고자 할 때 이것도 가능
        
        if old_password and new_password2:
            if old_password == new_password2:
                raise forms.ValidationError('새 암호는 기존 암호와 다르게 해주세요')
        return new_password2