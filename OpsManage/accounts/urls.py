from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editAdmin$', views.editAdmin),
    url(r'^setPassword$', views.setPassword),
    url(r'^newPasswordSubmit$',views.newPasswordSubmit),
    # url(r'^login',views.login_view),
]
