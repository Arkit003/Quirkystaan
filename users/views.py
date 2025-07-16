from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,UserRegistrationForm,ProfileEditForm,UserEditForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
# Create your views here.

@login_required
def index(request):
    current_user=request.user#we only want the post from current user
    posts=Post.objects.filter(user=current_user)
    profile=Profile.objects.filter(user=current_user).first()
    
    return render(request,'users/index.html',context={"posts":posts,'profile':profile})


def user_login(request):
    form=LoginForm#will directly get all the fields
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data#cleaning  up so no giberish get.
            user=authenticate(
                request,username=data['username'],password=data['password']
                )#returns an user object
            if user is not None:
                login(request,user)
                
                # return HttpResponse("user authenticated and logged in ")
                return redirect('feed')
            else:
                return HttpResponse("Invalid credentials")
        
    else:
        form=LoginForm()#this directly uses the get method
    return render(request,"users/login.html",context={"form":form})

def signup(request):
    #if the users sumbit the form we want to save it's info in db
    #so we will check for post request
    if request.method=="POST":
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            #commit=False so that we dont save the Password 
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)#creating the profile when the user signups
            return render(request,'users/signup_done.html',context={})
    else:
        user_form=UserRegistrationForm()
    return render(request,'users/signup.html',context={"user_form":user_form})

@login_required
def edit_profile(request):
    if request.method=="POST":
        edit_form=UserEditForm(instance=request.user,data=request.POST)#dont need the post method as we are fetching data
        profile_edit_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if edit_form.is_valid() and profile_edit_form.is_valid():
            edit_form.save()
            profile_edit_form.save()
    else:
        edit_form=UserEditForm(instance=request.user)#we keep instance to get the data from current user
        profile_edit_form=ProfileEditForm(instance=request.user.profile)
    return render(request,"users/edit_profile.html",context={
        "edit_form":edit_form,
        "profile_edit_form":profile_edit_form
    })