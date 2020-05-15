from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        widgets = {
            'caption': forms.Textarea,
        }