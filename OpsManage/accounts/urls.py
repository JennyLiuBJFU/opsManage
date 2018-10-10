from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editAdmin$', views.editAdmin),
    url(r'^manageUser$',views.manageUser),
    url(r'^addAdminSubmit$', views.addAdminSubmit),
    url(r'^editAdminSubmit$',views.editAdminSubmit),
    url(r'^setPassword$', views.setPassword),
    url(r'^newPasswordSubmit$',views.newPasswordSubmit)
]
