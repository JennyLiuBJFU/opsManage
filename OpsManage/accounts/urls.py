from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^editAdmin$', views.editAdmin),
    # url(r'^setPassword$', views.setPassword),
    url(r'^newPasswordSubmit$', views.newPasswordSubmit),
    url(r'^userManage', views.userManage, name='userManage'), #迁移过来
    url(r'addUserSubmit', views.addUserSubmit, name='addUserSubmit'),  #迁移过来
    url(r'userVerify',views.userVerify, name='userVerify'), #迁移过来
    url(r'^editAdminSubmit',views.editAdminSubmit, name='editAdminSubmit'), #迁移过来
]
