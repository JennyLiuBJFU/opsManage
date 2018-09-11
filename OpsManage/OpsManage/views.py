from django.shortcuts import render
import cmdb.models
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    return render (request,'login.html')


def loginSubmit(request):
    name=request.POST['username']
    pwd=request.POST['password']
    user= authenticate(username=name, password=pwd)
    print(user)
    print('########################Login successfully############################')
    if user is not None:
        login(request,user)
        print(user)
        Assets = cmdb.models.Asset.objects.all()
        print(Assets)
        Organizations = cmdb.models.Organization.objects.all()
        if request.user.is_superuser:
            Perm = 1
        else:
            Perm = 0
        context = {
            'USERNAME': str(request.user),
            'Perm': Perm,
            'Assets': Assets,
            'Organizations': Organizations
        }
        return render(request, 'cmdb/ServerManage/index.html', context)
    else:
        Flag=1
        return render(request,'login.html',{'Flag':Flag})

def logout_view(request):
    logout(request)
    print('########################Logout successfully############################')
    return render(request, 'login.html')