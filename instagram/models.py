import re
from django.conf import settings
from django.db import models
from django.urls import reverse

class BaseModel(models.Model):  # TODO core 앱에 모델로 처리해 볼 것
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_post_set')
    photo = models.ImageField()
    caption = models.CharField(max_length=500)
    location = models.CharField(max_length=50)
    tag_set = models.ManyToManyField('Tag', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_post_set')

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", kwargs={"pk": self.pk})
    
    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()
    
    class Meta:
        ordering = ['-id']

class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
