from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.template.loader import render_to_string

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        Male = 'M', '남성'
        Female = 'F', '여성'

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='accounts/profile/%Y/%m/%d', help_text='48px * 48px 크기의 png/jpeg 이미지를 업로드 해주세요')
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r'^010-?[0-9]\d{3}-?\d{4}$')])

    def send_welcome_email(self):
        
        subject = render_to_string('accounts/welcome_email_subject.txt', {
            "user": self,
        })
        content = render_to_string('accounts/welcome_email_content.txt', {
            "user": self,
        })        # subject = "instagram"

        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)