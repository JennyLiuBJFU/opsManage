from django.shortcuts import render, redirect, HttpResponse
import cmdb.models
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User Group
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from cmdb.models import Organization
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from  cmdb.operateLogs import WriteLog

def login_view(request):
    try:
        nextUrl = request.GET['next']
    except:
        nextUrl = '0'

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                print('########################Login successfully############################')
                if request.POST['nextUrl'] != '0':
                    url = 'http://127.0.0.1:8000' + request.POST['nextUrl']
                    url = url.replace('%3', '?')
                    url = url.replace('%3D', '=')
                    url = url.replace('%26', '&')
                    return redirect(url)
                else:
                    return redirect('/cmdb/')

            else:
                error = '用户或密码错误，请重新输入'
                return render(request, 'login.html', {'loginForm': login_form, 'login_error': error})

        else:
            return render(request, 'login.html', {'loginForm': login_form})

    if request.method == 'GET':
        obj = LoginForm()
        return render(request, 'login.html', {'loginForm': obj, 'nextUrl': nextUrl})



def logout_view(request):
    logout(request)
    print('########################Logout successfully############################')
    return redirect('/accounts/login/')



@login_required()
def editAdmin(request):
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'flag': 0,
    }
    return render(request, 'accounts/userEdit.html', context)


@login_required()
def setPassword(request):
    dadmin = request.POST.getlist('delete_admin')
    print(dadmin)
    if len(dadmin):
        for i in dadmin:
            User.objects.get(pk=i).delete()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    admin = User.objects.all()
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Flag': 1,
        'Perm': Perm,
    }
    return render(request, 'cmdb/ServerManage/index.html', context)


@login_required()
def newPasswordSubmit(request):
    Perm = 0
    if request.user.is_superuser:
        Perm = 1
    flag = 0
    if (request.POST['newPassword'] == request.POST['checkPassword']) and len(request.POST['newPassword']):
        request.user.set_password(request.POST['newPassword'])
        # name=request.user.username
        # pwd=request.POST['newPassword']
        request.user.save()
        # user = authenticate(username=name, password=pwd)
        # login(request, user)
        flag = 1  # 修改成功
    else:
        flag = 2  # 修改失败
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'flag': flag
    }
    return render(request, 'accounts/userEdit.html', context)


@login_required()
def userManage(request):
    if request.user.is_superuser:
        Perm = 1
        dadmin = request.POST.getlist('delete_admin')
        if len(dadmin):
            for i in dadmin:
                User.objects.get(pk=i).delete()
        USER=User.objects.get(username=request.user.username)

        org_incharge = []

        for i in USER.groups.all():
            organization=Organization.objects.get(org_name=i.name)
            org_incharge.append(organization) #自己
            for oSon in Organization.objects.filter(parent_org=organization):
                org_incharge.append(oSon) #子辈
                for oGrandSon in Organization.objects.filter(parent_org = oSon):
                    org_incharge.append(oGrandSon) #孙子辈
                    for oGrandGrandSon in Organization.objects.filter(parent_org = oGrandSon):
                        org_incharge.append(oGrandGrandSon) #重孙辈
        admin=[]
        groups=[]
        for ORG in org_incharge:
            GROUP=Group.objects.get(name=ORG.org_name)
            groups.append(GROUP)
            for g in GROUP.user_set.all():
                admin.append(g)
        # admin=User.objects.all()
        ADMIN = User()
        try:
            editID = request.GET['userId']
            if editID:
                ADMIN=User.objects.get(id=editID)
        except:
            print("没有userId参数")

        context = {
            'admin': admin,
            'USERNAME': str(request.user),
            'Perm': Perm,
            'tab_number': "user",
            "ADMIN": ADMIN,
            "groups": groups,
        }

        return render(request, 'accounts/userManage.html', context)

    else:
        return HttpResponse("对不起，您没有这个权限！")











'''
@login_required()
def userManage(request):
    dadmin = request.POST.getlist('delete_admin')
    if len(dadmin):
        for i in dadmin:
            User.objects.get(pk=i).delete()
    USER=User.objects.get(username=request.user.username)

    org_incharge = []

    for i in USER.groups.all():
        organization=Organization.objects.get(org_name=i.name)
        org_incharge.append(organization) #自己
        for oSon in Organization.objects.filter(parent_org=organization):
            org_incharge.append(oSon) #子辈
            for oGrandSon in Organization.objects.filter(parent_org = oSon):
                org_incharge.append(oGrandSon) #孙子辈
                for oGrandGrandSon in Organization.objects.filter(parent_org = oGrandSon):
                    org_incharge.append(oGrandGrandSon) #重孙辈
    admin=[]
    groups=[]
    for ORG in org_incharge:
        GROUP=Group.objects.get(name=ORG.org_name)
        groups.append(GROUP)
        for g in GROUP.user_set.all():
            admin.append(g)
    # admin=User.objects.all()
    ADMIN = User()
    try:
        editID = request.GET['userId']
        if editID:
            ADMIN=User.objects.get(id=editID)
    except:
        print("没有userId参数")
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Perm': Perm,
        'tab_number': "user",
        "ADMIN":ADMIN,
        "groups":groups,

    }
    return render(request,'accounts/userManage.html',context)
'''


@login_required()
def addUserSubmit(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    try :
        if str(request.POST['perm']) != '0':
            user.is_superuser = True
    except:
        print("不是管理员")
    if request.POST['group']!='0':
        GROUP=Group.objects.get(id=request.POST['group'])
        user.groups.add(GROUP)
        print(user.groups.all())
    user.save()
    # admin = User.objects.all()
    USER=User.objects.get(username=request.user.username)

    org_incharge = []

    for i in USER.groups.all():
        organization = Organization.objects.get(org_name=i.name)
        org_incharge.append(organization)  # 自己
        for oSon in Organization.objects.filter(parent_org=organization):
            org_incharge.append(oSon)  # 子辈
            for oGrandSon in Organization.objects.filter(parent_org=oSon):
                org_incharge.append(oGrandSon)  # 孙子辈
                for oGrandGrandSon in Organization.objects.filter(parent_org=oGrandSon):
                    org_incharge.append(oGrandGrandSon)  # 重孙辈
    admin = []
    groups = []
    for ORG in org_incharge:
        GROUP = Group.objects.get(name=ORG.org_name)
        groups.append(GROUP)
        for g in GROUP.user_set.all():
            admin.append(g)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Perm': Perm,
        "groups": groups,

    }
    return render(request,'accounts/userManage.html',context)


@login_required()
def userVerify(request):
    print(request.POST)
    USERNAME=request.POST['username']
    username=False
    users=User.objects.all()
    for user in users:
        if user.id != int(request.POST['userId']):
            if user.username == USERNAME:
                username=True
    response=JsonResponse({"username":username})
    return response


@login_required()
def editAdminSubmit(request):
    user=User.objects.get(id=request.GET['userId'])
    user.username=request.POST['username']
    user.email=request.POST['email']
    user.set_password(request.POST['password'])
    try :
        if str(request.POST['perm']) != '0':
            user.is_superuser = True
    except:
        print("不是管理员")
    if request.POST['group']!='0':
        GROUP=Group.objects.get(id=request.POST['group'])
        user.groups.clear()
        user.groups.add(GROUP)
        print(user.groups.all())
    user.save()
    # admin = User.objects.all()
    USER=User.objects.get(username=request.user.username)

    org_incharge = []

    for i in USER.groups.all():
        organization = Organization.objects.get(org_name=i.name)
        org_incharge.append(organization)  # 自己
        for oSon in Organization.objects.filter(parent_org=organization):
            org_incharge.append(oSon)  # 子辈
            for oGrandSon in Organization.objects.filter(parent_org=oSon):
                org_incharge.append(oGrandSon)  # 孙子辈
                for oGrandGrandSon in Organization.objects.filter(parent_org=oGrandSon):
                    org_incharge.append(oGrandGrandSon)  # 重孙辈
    admin = []
    groups = []
    for ORG in org_incharge:
        GROUP = Group.objects.get(name=ORG.org_name)
        groups.append(GROUP)
        for g in GROUP.user_set.all():
            admin.append(g)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Perm': Perm,
        "groups": groups,

    }
    return render(request, 'accounts/userManage.html', context)