from django import forms
from django.contrib.auth.forms import UserCreationForm
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
