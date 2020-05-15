from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, '새 포스팅을 작성하였습니다.')
            return redirect('/')    # TODO get_absolute_url 활용
    else:
        form = PostForm()
    return render(request, 'instagram/post_form.html', {
        'form': form
    })