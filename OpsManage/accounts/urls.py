from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editAdmin$', views.editAdmin),
    url(r'^setPassword$', views.setPassword),
    url(r'^newPasswordSubmit$',views.newPasswordSubmit),
<<<<<<< HEAD
    # url(r'^login',views.login_view),
=======
    url(r'^login',views.login_view)
>>>>>>> 53b3742e7d4905471f3e5d4ee6a4434903de179c
]
