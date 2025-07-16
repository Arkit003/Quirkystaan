from django.shortcuts import render,redirect
from .forms import PostCreateForm,CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required
def post_creation(request):
    if request.method=="POST":
        form=PostCreateForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            new_item=form.save(commit=False)#commit=False will not for now save the data to DB
            new_item.user=request.user#getting the user from currently logged in user
            new_item.save()
    else:
        form=PostCreateForm(data=request.GET)         
    return render(request,'posts/post_create.html',context={"form":form})

def feed(request):
    if request.method=="POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            post_id=request.POST.get('post_id')#we will get this from a hidden field in form
            post=get_object_or_404(Post,id=post_id)
            new_comment.post=post
            new_comment.user=request.user
            new_comment.save()
            return redirect('feed')
    else:
        comment_form=CommentForm()
        
    posts=Post.objects.all()
    logged_user=request.user
    return render(request,'posts/feed.html',context={
        "posts":posts,
        'logged_user':logged_user,
        'comment_form':comment_form
        })


def like_post(request):
    post_id=request.POST.get('post_id')
    post=get_object_or_404(Post,id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)    
        
    return redirect('feed') 