from django.shortcuts import render
import cmdb.models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    try:
        nextUrl=request.GET['next']
        print(nextUrl)

    except:
        nextUrl='0'
    context={
        'nextUrl':nextUrl,
    }
    return render (request,'login.html',context)

@login_required()
def editAdmin(request):
    if  request.user.is_superuser:
        Perm=1
    else:
        Perm=0
    print("*******************************************")
    context = {
        'USERNAME':str(request.user),
        'Perm':Perm,
        'flag':0,
    }
    return render(request, 'accounts/userEdit.html', context)

@login_required()
def setPassword(request):
    dadmin = request.POST.getlist('delete_admin')
    print(dadmin)
    if len(dadmin):
        for i in dadmin:
            User.objects.get(pk=i).delete()
    if  request.user.is_superuser:
        Perm=1
    else:
        Perm=0
    admin = User.objects.all()
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Flag':1,
        'Perm':Perm,
    }
    return render(request, 'cmdb/ServerManage/index.html', context)

@login_required()
def newPasswordSubmit(request):
    Perm = 0
    if request.user.is_superuser:
        Perm = 1
    flag=0
    if(request.POST['newPassword']==request.POST['checkPassword']) and len(request.POST['newPassword']):
        request.user.set_password(request.POST['newPassword'])
        # name=request.user.username
        # pwd=request.POST['newPassword']
        request.user.save()
        # user = authenticate(username=name, password=pwd)
        # login(request, user)
        flag=1   #修改成功
    else:
        flag=2  #修改失败
    context = {
        'USERNAME': str(request.user),
        'Perm':Perm,
        'flag':flag
    }
    return render(request, 'accounts/userEdit.html', context)

