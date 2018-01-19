from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    # 根据给定的模型和字段创建表单
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # 格式如claean_<fieldname>的方法会在表单执行is_valid方法时被调用。这样可以来校验一些字段
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')