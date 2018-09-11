from django.shortcuts import render
import cmdb.models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

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
    return render(request, 'accounts/userEdit.html', context)

@login_required()
def newPasswordSubmit(request):
    Perm = 0
    if(request.POST['newPassword']==request.POST['checkPassword']) and len(request.POST['newPassword']):
        request.user.set_password(request.POST['newPassword'])
        name=request.user.username
        pwd=request.POST['newPassword']
        request.user.save()
        user = authenticate(username=name, password=pwd)
        login(request, user)
        flag=1
        if request.user.is_superuser:
            Perm = 1
    else:
        flag=0
    context = {
        'USERNAME': str(request.user),
        'Flag': 0,
        'flag':flag,
        'Perm':Perm,
    }
    return render(request, 'accounts/userEdit.html', context)

@login_required()
def manageUser(request):
    dadmin = request.POST.getlist('delete_admin')
    print(dadmin)
    print(Permission.objects.all())
    if len(dadmin):
        for i in dadmin:
            User.objects.get(pk=i).delete()

    admin = User.objects.all()
    context = {
        'admin': admin,
        'USERNAME': str(request.user)
    }
    return render(request, 'accounts/manageUser.html', context)


@login_required()
def addAdminSubmit(request):
    user=User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
    print(request.POST['perm'])
    print(type(request.POST['perm']))
    if str(request.POST['perm'])!='0':
        user.is_superuser=True
    user.save()
    admin = User.objects.all()
    context = {
        'admin': admin
    }

    return render(request, 'accounts/manageUser.html', context)

@login_required()
def addAdminBack(request):
    Assets = cmdb.models.Asset.objects.all()
    Organizations = cmdb.models.Organization.objects.all()
    context = {
        'Assets': Assets,
        'Organizations': Organizations
    }
    return render(request, 'cmdb/ServerManage/index.html', context)


