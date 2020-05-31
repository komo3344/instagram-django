from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import PostForm, CommentForm
from .models import Post, Comment

@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
                .filter(
                    Q(author=request.user ) |
                    Q(author__in=request.user.following_set.all())
                )\
                .filter(
                    created_at__gte=timesince
                )
    suggested_user_list = get_user_model().objects.all()\
                        .exclude(pk=request.user.pk)\
                        .exclude(pk__in=request.user.following_set.all())[:3]

    comment_form = CommentForm()

    return render(request, 'instagram/index.html', {
        'post_list': post_list,
        'suggested_user_list': suggested_user_list,
        'comment_form': comment_form
    })

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, '새 포스팅을 작성하였습니다.')
            return redirect(post)    # TODO get_absolute_url 활용
    else:
        form = PostForm()
    return render(request, 'instagram/post_form.html', {
        'form': form
    })

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, 'instagram/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root") # 양식이 제출된 페이지로 이동 없으면 root
    return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"#{post.pk} 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()
    return render(request, 'instagram/user_page.html', {
        'page_user': page_user, 'post_list': post_list, 'post_list_count': post_list_count, 'is_follow': is_follow
    })

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.post) # post 모델 객체로 이동
    else:
        form = CommentForm()
    return render(request, 'instagram/comment_form.html', {
        'form': form
    })