# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done, password_reset, \
                                        password_reset_done, password_reset_confirm, password_reset_complete
from . import views



urlpatterns = [
    # 自定义的登录
    # url(r'^login/$', views.user_login, name='login'),

    # authentication框架自带的登录登出，修改密码，重置密码
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', password_change, name='password_change'),   # registration/password_change_form.html
    url(r'^password-change-done/$', password_change_done, name='password_change_done'),   # registration/password_change_done.html
    url(r'^password-reset/$', password_reset, name='password_reset'),   # 这个页面是填写email
    url(r'^password-reset-done/', password_reset_done, name='password_reset_done'),   # 提示email发送成功
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),   # 邮件里面的链接
    url(r'^password-reset-complete/', password_reset_complete, name='password_reset_complete'),   # 输入两次新密码后的完成提示

    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
]