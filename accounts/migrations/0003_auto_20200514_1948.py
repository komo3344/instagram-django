# Generated by Django 3.0.6 on 2020-05-14 19:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200514_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator('^010-?[1-9]\\d{3}-?\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='48px * 48px 크기의 png/jpeg 이미지를 업로드 해주세요', upload_to='accounts/profile/%Y/%m/%d'),
        ),
    ]
