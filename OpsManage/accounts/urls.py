from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editAdmin$', views.editAdmin),
    url(r'^setPassword$', views.setPassword),
    url(r'^newPasswordSubmit$',views.newPasswordSubmit),
<<<<<<< HEAD
    # url(r'^login',views.login_view),
=======

>>>>>>> cd7270b9dbb2e48298ca3b2a92b4784577ddfc53
    url(r'^login',views.login_view)

]
