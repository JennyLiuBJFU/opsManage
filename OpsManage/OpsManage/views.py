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
        # 查询中线局对象
        zxj = cmdb.models.Organization.objects.get(org_name="中线局")
        zxj_children = []

        # 查询分局局对象
        fenju_list = cmdb.models.Organization.objects.filter(parent_org=zxj.id)

        # 生成各级组织名称
        for fenju in fenju_list:
            guanlichu_list = cmdb.models.Organization.objects.filter(parent_org=fenju.id)
            # print(guanlichu_list)
            fenju_name = fenju.org_name
            list_tmp = []
            for guanlichu in guanlichu_list:
                xiandizhan_list = cmdb.models.Organization.objects.filter(parent_org=guanlichu.id)
                xiandizhan_name = guanlichu.org_name
                xdz_list = []
                for xindizhan in xiandizhan_list:
                    xdz_context = {"name": xindizhan.org_name}
                    xdz_list.append(xdz_context)
                glc_context = {"name": xiandizhan_name, "children": xdz_list}
                list_tmp.append(glc_context)
            fenju_children = {"name": fenju_name, "children": list_tmp}
            zxj_children.append(fenju_children)
        org_dic = {"name": zxj.org_name, "children": zxj_children}
        if request.user.is_superuser:
            Perm = 1
        else:
            Perm = 0
        context = {
            'USERNAME': str(request.user),
            'Perm': Perm,
            'data': org_dic,
        }
        return render(request, 'cmdb/index.html', context)
<<<<<<< HEAD
=======

>>>>>>> 342a308b5056210cb6149090e3a26a8e3c3fa9b7
    else:
        Flag=1
        return render(request,'login.html',{'Flag':Flag})

def logout_view(request):
    logout(request)
    print('########################Logout successfully############################')
    return render(request, 'login.html')