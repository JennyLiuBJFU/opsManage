from django.shortcuts import render
import cmdb.models
from django.contrib.auth import authenticate, login, logout
from cmdb.import_org import import_org_info
from cmdb.import_asset import import_server_info,import_VM_info



def login_view(request):
    return render (request,'login.html')


def loginSubmit(request):
    import_server_info()
    import_VM_info()
    name=request.POST['username']
    pwd=request.POST['password']
    user= authenticate(username=name, password=pwd)
    print('########################Login successfully############################')
    if user is not None:
        login(request,user)
        print(user)
        orglist = cmdb.models.Organization.objects.all()
        Assets = list(cmdb.models.Asset.objects.all())

        # ------树形图数据计算，排出各单位及其子单位的列表--------
        zxj = cmdb.models.Organization.objects.get(org_name="中线局")
        zxj_children = []
        # 查询分局局对象
        fenju_list = cmdb.models.Organization.objects.filter(parent_org=zxj.id)
        # 生成各级组织名称
        for fenju in fenju_list:
            guanlichu_list = cmdb.models.Organization.objects.filter(parent_org=fenju.id)
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

        hebei = cmdb.models.Organization.objects.get(org_name="河北分局")
        beijing = cmdb.models.Organization.objects.get(org_name="北京分局")
        tianjin = cmdb.models.Organization.objects.get(org_name="天津分局")

        def seachchildren2(org, orglist, Assets):
            children_list = []
            server_count = 0
            network_count = 0
            security_count = 0
            storage_count = 0

            for i in orglist:
                try:
                    if (i == org):
                        children_list.append(i)
                    if (i.parent_org == org):
                        children_list.append(i)
                    if i.parent_org.parent_org == org:
                        children_list.append(i)
                except AttributeError:
                    print(AttributeError)

            for a in Assets:
                for o in children_list:
                    if (a.organization == o):
                        if (a.asset_type == "1"):
                             server_count += 1
                        if (a.asset_type == "2"):
                            network_count += 1
                        if (a.asset_type == "3"):
                            security_count += 1
                        if (a.asset_type == "4"):
                            storage_count += 1
            return server_count, network_count, security_count, storage_count

        tj_server_count, tj_network_count, tj_security_count, tj_storage_count = seachchildren2(tianjin, orglist,
                                                                                                    Assets)
        hb_server_count, hb_network_count, hb_security_count, hb_storage_count = seachchildren2(hebei, orglist,
                                                                                                    Assets)
        bj_server_count, bj_network_count, bj_security_count, bj_storage_count = seachchildren2(beijing, orglist,
                                                                                                    Assets)

        zxj_server_count = 0
        zxj_network_count = 0
        zxj_security_count = 0
        zxj_storage_count = 0

        for obj in Assets:
            if obj.organization == zxj:
                if obj.asset_type == "1":
                    zxj_server_count += 1
                if obj.asset_type == "2":
                    zxj_network_count += 1
                if obj.asset_type == "3":
                    zxj_security_count += 1
                if obj.asset_type == "4":
                    zxj_storage_count += 1

        # ------统计中线局个类设备数量-------
        server_total = 0
        network_total = 0
        security_total = 0
        storage_total = 0

        for obj in Assets:
            if obj.asset_type == "1":
                server_total += 1
            if obj.asset_type == "2":
                network_total += 1
            if obj.asset_type == "3":
                security_total += 1
            if obj.asset_type == "4":
                storage_total += 1
        if request.user.is_superuser:
            Perm = 1
        else:
            Perm = 0
        context = {
            'USERNAME': str(request.user),
            'Perm': Perm,
            'org_data': org_dic,
            'asset_total': len(Assets),
            'server_total': server_total,
            'network_total': network_total,
            'security_total': security_total,
            'storage_total': storage_total,
            'tj_server_count': tj_server_count,
            'tj_network_count': tj_network_count,
            'tj_security_count': tj_security_count,
            'tj_storage_count': tj_storage_count,
            'bj_server_count': bj_server_count,
            'bj_network_count': bj_network_count,
             'bj_security_count': bj_security_count,
            'bj_storage_count': bj_storage_count,
            'hb_server_count': hb_server_count,
            'hb_network_count': hb_network_count,
            'hb_security_count': hb_security_count,
            'hb_storage_count': hb_storage_count,
            'zxj_server_count': zxj_server_count,
            'zxj_network_count': zxj_network_count,
            'zxj_security_count': zxj_security_count,
            'zxj_storage_count': zxj_storage_count,
        }
        return render(request, 'cmdb/index.html', context)

    else:
        Flag=1
        return render(request,'login.html',{'Flag':Flag})

def logout_view(request):
    logout(request)
    print('########################Logout successfully############################')
    return render(request, 'login.html')