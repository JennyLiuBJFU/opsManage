from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editAdmin$', views.editAdmin),
    url(r'^manageUser$',views.manageUser),
    url(r'^addAdminSubmit$', views.addAdminSubmit),
    url(r'^newPasswordSubmit$',views.newPasswordSubmit)
]
