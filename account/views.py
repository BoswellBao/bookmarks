from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile



# 自定义的登录视图，可以用authentication框架自带的登录视图
def user_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

# login_required装饰器能够校验用户的登录状态，并提供登录重定向的功能
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 创建一个暂不保存的用户对象
            new_user = user_form.save(commit=False)
            # 给用户设置密码，之前还没有设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存用户
            new_user.save()
            # 创建用户简介
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

# login_required装饰器能够校验用户的登录状态，并提供登录重定向的功能
@login_required
def edit(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(instance=request.user, data=request.POST)
        profile_edit_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            # messages给出提示信息
            messages.add_message(request, messages.SUCCESS, 'success')   # 与messages.success(request,'success')一样
        else:
            messages.error(request, 'Profile updated unsuccessfully')
    else:
        user_edit_form = UserEditForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_edit_form':user_edit_form,
                                                 'profile_edit_form':profile_edit_form})
