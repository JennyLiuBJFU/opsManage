# -*- coding: utf-8 -*-


from  django.core.paginator import *
import json
from django.shortcuts import render
from django.http import HttpResponse
from cmdb.models import *
from django.contrib.auth.decorators import login_required
import numpy
import qrcode
from django.utils.six import BytesIO
from django.http import JsonResponse
from  django.db.models import Q
from django.shortcuts import HttpResponse, render, redirect


# 分页函数
def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 4 if current - 6 > 0 else 1
    max_page = min_page + 6 if min_page + 6 < total else total
    return range(min_page, max_page + 1)

# 分页函数
def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    page_len = request.GET.get('page_len', '')
    if not page_len:
        page_len = 20
    paginator = Paginator(post_objects, page_len)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)
    end_page = len(paginator.page_range)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    offset_index = (current_page - 1)*int(page_len)

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页,每页对象序号偏移值
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end, end_page, offset_index


def asset(request):
    USERNAME = str(request.user)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    asset_find=[]

    page_len = request.GET.get('page_len', '')
    Organizations = Organization.objects.all()

    #查询关键字列表
    myType = int(request.GET.get('myType', "0"))
    myOrg = int(request.GET.get('myOrg', "0"))
    myNet = int(request.GET.get('myNet', "0"))

    search_dict = dict()  # 如果有这个值 就写入到字典中去
    if myType != 0:
       search_dict['asset_type'] = myType
    if myOrg != 0:
       search_dict['organization'] = myOrg
    if myNet != 0:
       search_dict['network_location'] = myNet

    if len(asset_find) >= 0:
        asset_find = Asset.objects.filter(**search_dict)
    else:
        asset_find = Asset.objects.all()

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    assets_list, p, assets, page_range, current_page, show_first, show_end, end_page, offset_index = pages(asset_find, request)
    print("-------------------")
    print(offset_index)
    return render(request, 'cmdb/ServerManage/asset.html', locals())




def index(request):
    orglist =Organization.objects.all()
    Assets = list(Asset.objects.all())

    # ------树形图数据计算，排出各单位及其子单位的列表--------
    zxj = Organization.objects.get(org_name="中线局")
    zxj_children = []
    # 查询分局局对象
    fenju_list = Organization.objects.filter(parent_org=zxj.id)
    #生成各级组织名称
    for fenju in fenju_list:
        guanlichu_list = Organization.objects.filter(parent_org=fenju.id)
        fenju_name = fenju.org_name
        list_tmp = []
        for guanlichu in guanlichu_list:
            xiandizhan_list = Organization.objects.filter(parent_org=guanlichu.id)
            xiandizhan_name = guanlichu.org_name
            xdz_list = []
            for xindizhan in xiandizhan_list:
                xdz_context = {"name": xindizhan.org_name}
                xdz_list.append(xdz_context)
            glc_context = {"name": xiandizhan_name,"children":xdz_list}
            list_tmp.append(glc_context)
        fenju_children = {"name":fenju_name,"children":list_tmp}
        zxj_children.append(fenju_children)
    org_dic = {"name":zxj.org_name,"children": zxj_children}
    # /树形图数据计算，排出各单位及其子单位的列表


    #--------柱形表数据构造--------------------
    hebei = Organization.objects.get(org_name="河北分局")
    beijing = Organization.objects.get(org_name="北京分局")
    tianjin = Organization.objects.get(org_name="天津分局")

    #查询子单位
    # def seachchildren(org,orglist):
    #     children_list = []
    #     for child in orglist:
    #         if child.parent_org == org:
    #             children_list.append(child)
    #     return children_list

    #查询子单位、孙单位
    def seachchildren2(org, orglist,Assets):
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
                print("组织")
                print(o)
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

    tj_server_count, tj_network_count, tj_security_count, tj_storage_count = seachchildren2(tianjin, orglist, Assets)
    hb_server_count, hb_network_count, hb_security_count, hb_storage_count = seachchildren2(hebei, orglist, Assets)
    bj_server_count, bj_network_count, bj_security_count, bj_storage_count = seachchildren2(beijing, orglist, Assets)

    #------统计中线局个类设备数量-------
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

    #------统计中线局个类设备数量-------
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


    context = {
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


@login_required()
def addARecord(request):
    Vendors = Vendor.objects.all()
    Organizations = Organization.objects.all()
    Users=User.objects.all()
    Contracts=Contract.objects.all()
    Suppliers=Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Vendors': Vendors,
        'Organizations': Organizations,
        'Users':Users,
        'Contracts':Contracts,
        'Suppliers':Suppliers,
    }
    return render(request, 'cmdb/ServerManage/add/add.html', context)

@login_required()
def showidcs(request, id):
    org = id
    Idcs=Idc.objects.filter(organization_id=org)
    list = []
    for idc in Idcs:
        list.append({"id":idc.id, "idc":idc.idc_name})
    return JsonResponse({"data": list})

@login_required()
def showcabs(request, id):
    IDC=id
    cabs=Cabinet.objects.filter(idc=IDC)
    list=[]
    for cab in cabs:
       list.append({"id": cab.id, "cab": cab.cabinet_name})
    print(list)
    return JsonResponse({"data": list})

@login_required()
def showcabspace(request, id):
    cab_id = id
    CabSpaces=CabinetSpace.objects.filter(cabinet_id=cab_id)
    list = []
    t = "disabled"
    f = ""
    # 数据格式{"id": 1, "space": space, "used": True}
    for cs in CabSpaces:
        temp = cs.get_cabinet_location_display()
        if cs.asset == None:
            list.append({"id": cs.id, "space": temp, "useinfo": f,})
        else:
            list.append({"id": cs.id, "space": temp, "useinfo": t,})


    return JsonResponse({"data":list})


@login_required()
def addSubmit(request):
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    #创建资产对象
    ASSET=Asset()

    # 把text类型的7个值保存到资产对象
    ASSET.asset_name = request.POST['asset_name']
    ASSET.manage_ip = request.POST['manage_ip']
    ASSET.memo = request.POST['memo']
    ASSET.asset_no = request.POST['asset_no']
    ASSET.sn = request.POST['sn']
    ASSET.expire_day = request.POST['expire_day']
    ASSET.purchase_day = request.POST['purchase_day']

    # 把直接select标签的3个值保存到资产对象
    if request.POST['status'] != "0":
        ASSET.status = request.POST['status']
    if request.POST['network_location'] != "0":
        ASSET.network_location = request.POST['network_location']
    if request.POST['asset_type'] != "0":
        ASSET.asset_type = request.POST['asset_type']

    # 把外键的7个值保存到资产对象
    if request.POST['admin'] != "0":
        ASSET.admin = User.objects.get(id=request.POST['admin'])
    if request.POST['model'] != "0":
        ASSET.model = Device_model.objects.get(id=request.POST['model'])
    if request.POST['contract'] != "0":
        ASSET.contract = Contract.objects.get(id=request.POST['contract'])
    if request.POST['supplier'] != "0":
        ASSET.supplier = Supplier.objects.get(id=request.POST['supplier'])
    if request.POST['organization'] != "0":
        ASSET.organization = Organization.objects.get(id=request.POST['organization'])
    if request.POST['approved_by'] != "0":
        ASSET.approved_by = User.objects.get(id=request.POST['approved_by'])
    if request.POST['idc'] != "0":
        ASSET.idc = Idc.objects.get(id=request.POST['idc'])
    if request.POST['cabinet'] != "0":
        ASSET.cabinet = Cabinet.objects.get(id=request.POST['cabinet'])
    ASSET.save()


    #生成机柜空间
    CapSpasId = request.POST.getlist('cabSpace')
    num = 0
    hPlace = 0
    if CapSpasId:
        for cId in CapSpasId:
            num = num + 1
            CABSPACE = CabinetSpace.objects.get(id=cId)
            if int(CABSPACE.cabinet_location) > hPlace:
                hPlace = int(CABSPACE.cabinet_location)
            CABSPACE.asset = ASSET
            CABSPACE.save()
        ASSET.height = num * 22 - 2
        ASSET.cab_location = ASSET.cabinet.cabinet_height - hPlace
    ASSET.save()


    #生成设备的二维码
    obj_url = "http://127.0.0.1/cmdb/detail" + str(ASSET.id)
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=8,
                       border=2,
                       )
    qr.add_data(obj_url)
    qr.make(fit=True)
    img = qr.make_image()
    img_name = 'media/QRcode_imgs/' + ASSET.asset_name + '.png'
    img.save(img_name)
    ASSET.qrcode = img_name
    ASSET.save()
    # 生成二维码完毕

    #生成给下一个页面的信息
    vendor = Vendor.objects.get(id=request.POST['vendor']).vendor_name
    asset_type = request.POST['asset_type']
    asset_subtype = request.POST['asset_subtype']
    asset_type_display = ASSET.get_asset_type_display
    if ASSET.asset_type =='1':
        asset_subtype_display = Server.sub_asset_type_choice[int(asset_subtype)-1][1]
    else:
        asset_subtype_display=None

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ASSET.id,
        'asset_type':asset_type,
        'asset_type_display':asset_type_display,
        'asset_subtype':asset_subtype,
        'asset_subtype_display':asset_subtype_display,
        'vendor':vendor,
        "sn":request.POST['sn'],
        'model':Device_model.objects.get(id=request.POST['model']).models,
    }
    if ASSET.asset_type=='1':
        return render(request,'cmdb/ServerManage/add/addOneToOne/addServer.html',context)
    elif ASSET.asset_type=='2':
        NETWORKDEVICE=NetworkDevice()
        NETWORKDEVICE.asset=ASSET
        NETWORKDEVICE.sub_asset_type=asset_subtype
        NETWORKDEVICE.save()
        return render(request, 'cmdb/ServerManage/add/addMore.html', context)
    elif ASSET.asset_type=='3':
        SECURITYDEVICE=SecurityDevice()
        SECURITYDEVICE.asset=ASSET
        SECURITYDEVICE.sub_asset_type=asset_subtype
        return render(request, 'cmdb/ServerManage/add/addMore.html', context)
    elif ASSET.asset_type=='4':
        STORAGEDEVICE=StorageDevice()
        STORAGEDEVICE.asset=ASSET
        STORAGEDEVICE.sub_asset_type=asset_subtype
        return render(request, 'cmdb/ServerManage/add/addMore.html', context)
    else:
        return render(request, 'cmdb/ServerManage/add/addMore.html', context)


def editMore(request):
    ID=request.GET['assetId']
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus=CPU.objects.filter(asset=ASSET)
    disks=Disk.objects.filter(asset=ASSET)
    ports=Port.objects.filter(asset=ASSET)
    parts=Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context={
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'rams':rams,
        'cpus':cpus,
        'disks':disks,
        'ports':ports,
        'parts':parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def RAMSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    ram=RAM()
    ram.asset=ASSET
    ram.ram_model=request.POST['model']
    ram.ram_brand=request.POST['brand']
    ram.ram_volume=request.POST['volume']
    ram.ram_slot=request.POST['slot']
    ram.ram_status=request.POST['status']
    ram.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def RAMDelete(request):
    ID=request.GET['assetId']
    ram=RAM.objects.get(id=request.GET['ramId'])
    print(ram)
    ram.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def CPUSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    cpu=CPU()
    cpu.asset=ASSET
    cpu.cpu_model=request.POST['model']
    cpu.cpu_brand=request.POST['brand']
    cpu.cpu_speed=request.POST['speed']
    cpu.cpu_core_count=request.POST['core_count']
    cpu.cpu_slot=request.POST['slot']
    cpu.cpu_status=request.POST['status']
    cpu.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def CPUDelete(request):
    ID=request.GET['assetId']
    cpu=CPU.objects.get(id=request.GET['cpuId'])
    cpu.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def DiskSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    disk=Disk()
    disk.asset=ASSET
    disk.disk_name=request.POST['name']
    disk.disk_volume=request.POST['volume']
    disk.disk_model=request.POST['model']
    disk.disk_brand=request.POST['brand']
    disk.disk_serial=request.POST['serial']
    disk.disk_slot=request.POST['slot']
    disk.disk_status=request.POST['status']
    disk.disk_attr=request.POST['attr']
    disk.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def DiskDelete(request):
    ID=request.GET['assetId']
    disk=Disk.objects.get(id=request.GET['diskId'])
    disk.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def PortSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    port=Port()
    port.asset=ASSET
    port.port_type=request.POST['type']
    port.port_name=request.POST['name']
    port.port_slot=request.POST['slot']
    port.vlan=request.POST['vlan']
    port.ip=request.POST['ip']
    port.sub_ip=request.POST['sub_ip']
    port.mask=request.POST['mask']
    port.bandwidth=request.POST['bandwidth']
    port.status=request.POST['status']
    port.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def PortDelete(request):
    ID=request.GET['assetId']
    port=Port.objects.get(id=request.GET['portId'])
    port.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def PartSubmit(request):
    print(request.POST)
    ID = request.POST['assetId']
    ASSET=Asset.objects.get(id=ID)
    part=Parts()
    part.asset=ASSET
    part.parts_type=request.POST['type']
    part.parts_name=request.POST['name']
    part.parts_model=request.POST['model']
    part.parts_sn=request.POST['sn']
    part.parts_slot=request.POST['slot']
    part.parts_status=request.POST['status']
    part.memo=request.POST['partDesc']
    part.save()
    rams = RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request,'cmdb/ServerManage/add/addMore.html',context)

@login_required()
def PartDelete(request):
    ID=request.GET['assetId']
    part=Parts.objects.get(id=request.GET['partId'])
    part.delete()
    ASSET=Asset.objects.get(id=ID)
    rams=RAM.objects.filter(asset=ASSET)
    cpus = CPU.objects.filter(asset=ASSET)
    disks = Disk.objects.filter(asset=ASSET)
    ports = Port.objects.filter(asset=ASSET)
    parts = Parts.objects.filter(asset=ASSET)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID': ID,
        'rams': rams,
        'cpus': cpus,
        'disks': disks,
        'ports': ports,
        'parts': parts,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def serverSubmit(request):
    print(request.POST)
    ASSET=Asset.objects.get(id=request.POST['assetId'])
    SERVER=Server()
    SERVER.asset=ASSET
    SERVER.created_by="2"
    if request.POST['hosted_on'] != '0':
        SERVER.hosted_on=Server.objects.get(id=request.POST['hosted_on'])
    else:
        SERVER.hosted_on=None
    if request.POST['sub_asset_type'] != '0':
        SERVER.sub_asset_type=request.POST['sub_asset_type']
    else:
        SERVER.sub_asset_type=None
    if request.POST['os_type'] != '0':
        SERVER.os_type = request.POST['os_type']
    else:
        SERVER.os_type=None
    SERVER.microcode=request.POST['microcode']
    SERVER.os_distribution=request.POST['os_distribution']
    SERVER.os_release=request.POST['os_release']
    SERVER.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations':Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)


@login_required()
def networkDeviceSubmit (request):
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0

    ASSET = Asset.objects.get(id=request.POST['asset_id'])
    NETWORKDEVICE = NetworkDevice()
    if request.POST['asset_subtype'] != '0':
        NETWORKDEVICE.sub_asset_type=request.POST['asset_subtype']
    else:
        NETWORKDEVICE.sub_asset_type = None
    NETWORKDEVICE.asset=ASSET
    NETWORKDEVICE.save()

    # Organizations = Organization.objects.all()
    # ID=request.POST['asset_id']

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':request.POST['asset_id'],
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

#
# @login_required()
# def networkDeviceSubmit (request):
#     print(request.POST)
#     ASSET = Asset.objects.get(id=request.POST['assetId'])
#     NETWORKDEVICE=NetworkDevice()
#     NETWORKDEVICE.asset=ASSET
#     if request.POST['sub_asset_type'] != '0':
#         NETWORKDEVICE.sub_asset_type=request.POST['sub_asset_type']
#     else:
#         NETWORKDEVICE.sub_asset_type=None
#     NETWORKDEVICE.save()
#     Assets = Asset.objects.all()
#     Organizations = Organization.objects.all()
#     ID=request.POST['assetId']
#     if request.user.is_superuser:
#         Perm = 1
#     else:
#         Perm = 0
#     context = {
#         'USERNAME': str(request.user),
#         'Perm': Perm,
#         'ID':ID,
#         'Assets': Assets,
#         'Organizations':Organizations,
#     }
#     return render(request, 'cmdb/ServerManage/add/addMore.html', context)


@login_required()
def storageDeviceSubmit(request):
    print(request.POST)
    ASSET = Asset.objects.get(id=request.POST['assetId'])
    STORAGEDEVICE = StorageDevice()
    STORAGEDEVICE.asset = ASSET
    if request.POST['sub_asset_type'] != '0':
        STORAGEDEVICE.sub_asset_type = request.POST['sub_asset_type']
    else:
        STORAGEDEVICE.sub_asset_type=None
    STORAGEDEVICE.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)

@login_required()
def securityDeviceSubmit(request):
    print(request.POST)
    ASSET = Asset.objects.get(id=request.POST['assetId'])
    SECURITYDEVICE = SecurityDevice()
    SECURITYDEVICE.asset = ASSET
    if request.POST['sub_asset_type'] != '0':
        SECURITYDEVICE.sub_asset_type = request.POST['sub_asset_type']
    else:
        SECURITYDEVICE.sub_asset_type=None
    SECURITYDEVICE.memo=request.POST['memo']
    SECURITYDEVICE.save()
    Assets = Asset.objects.all()
    Organizations = Organization.objects.all()
    ID=request.POST['assetId']
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ID':ID,
        'Assets': Assets,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/ServerManage/add/addMore.html', context)


def detail(request, v):
    print(request)
    ASSET = Asset.objects.get(id=v)

    # 组装机柜空间
    SpaceList = []
    for i in ASSET.cabinetspace_set.values_list():
        SpaceList.append(int(i[3]))

    if len(SpaceList) >= 2:
        max = str(numpy.max(SpaceList))
        min = str(numpy.min(SpaceList))
        CabinetSpace = min +'U' + '--' + max + 'U'
    elif len(SpaceList) == 1:
        CabinetSpace = str(SpaceList[0]) + 'U'
    else:
        CabinetSpace = None

    #判断是否为超级用户
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0




    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ASSET': ASSET,
        'CabinetSpace': CabinetSpace,
    }
    return render(request, 'cmdb/detail.html', context)



@login_required()
def editModel(request):
    # 判断是否有删除请求，有则删除厂商
    dmodel = request.POST.getlist('delete_model')
    if len(dmodel):
        for i in dmodel:

            Device_model.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    model = Device_model.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'model': model,
        'vendors':vendors,
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editModel.html', context)

@login_required()
def addModelSubmit(request):
    o = Device_model()
    o.img=request.FILES.get('image')
    # o.vendor=request.POST['telephone']
    o.models=request.POST['models']
    o.save()
    model = Device_model.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'model': model,
        'vendors':vendors,
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editModel.html', context)


def editVendor(request):
    # 判断是否有删除请求，有则删除厂商
    dvendor = request.POST.getlist('delete_vendor')
    print(dvendor)
    if len(dvendor):
        for i in dvendor:
           Vendor.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor,
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editVendor.html',context)

@login_required()
def addVendorSubmit(request):
    o = Vendor()
    o.vendor_name=request.POST['name']
    o.vendor_phone=request.POST['phone']
    o.vendor_memo=request.POST['memo']
    o.save()
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editVendor.html', context)

@login_required()
def editSupplier(request):
    # 判断是否有删除请求，有则删除厂商
    dsupplier = request.POST.getlist('delete_supplier')
    if len(dsupplier):
        for i in dsupplier:
            Supplier.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier
    }
    return render(request, 'cmdb/ServerManage/add/editForeignKey/editSupplier.html',context)

@login_required()
def addSupplierSubmit(request):
    o = Supplier()
    o.supplier_name = request.POST['name']
    o.supplier_contacts = request.POST['contact']
    o.supplier_phone = request.POST['phone']
    o.supplier_memo = request.POST['memo']
    o.save()
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier
    }

    return render(request, 'cmdb/ServerManage/add/editForeignKey/editSupplier.html', context)

@login_required()
def deleteARecord(request):
    v = request.GET['myid']
    Asset.objects.get(id=v).delete()
    Assets = Asset.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Assets':Assets,
    }
    return render(request, 'cmdb/ServerManage/asset.html', context)

@login_required()
def editARecord(request):
    v = request.GET['myid']
    ASSET=Asset.objects.get(id=v)
    Vendors = Vendor.objects.all()
    Organizations = Organization.objects.all()
    # Tags = Tag.objects.all()
    Users = User.objects.all()
    IDCs = Idc.objects.filter(organization=ASSET.organization)
    Cabinets=Cabinet.objects.filter(idc=ASSET.idc)
    CabSpaces=CabinetSpace.objects.filter(cabinet=ASSET.cabinet,asset=None)
    listc = []
    for cs in CabSpaces:
        listc.append(cs)

    for i in range(len(listc) - 1):
        for j in range(len(listc) - i - 1):
            if int(listc[j].cabinet_location) < int(listc[j + 1].cabinet_location):
                listc[j], listc[j + 1] = listc[j + 1], listc[j]

    CSSelected=CabinetSpace.objects.filter(asset=ASSET)
    print("!!!!!!!!!!!!!!!!!!!!!!!")
    print(CSSelected)
    Contracts = Contract.objects.all()
    Suppliers = Supplier.objects.all()
    Servers=Server.objects.all()
    Models=Device_model.objects.all()

    PURCHASE_DAY=str(ASSET.purchase_day)
    EXPIRE_DAY=str(ASSET.expire_day)
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'Models':Models,
        'Cabinets':Cabinets,
        'CabSpaces':listc,
        'CSSelected':CSSelected,
        'Vendors': Vendors,
        'Organizations': Organizations,
        # 'Tags': Tags,
        'Users': Users,
        'IDCs': IDCs,
        'Contracts': Contracts,
        'Suppliers': Suppliers,
        'ASSET': ASSET,
        'ID':v,
        'PURCHASE_DAY':PURCHASE_DAY,
        'EXPIRE_DAY':EXPIRE_DAY,
        'Servers':Servers,
    }
    return render(request, 'cmdb/ServerManage/edit/editARecord.html', context)

@login_required()
def editSubmit(request):

    print(request.POST)
    print(len(request.POST))

    ASSET=Asset.objects.get(id=request.GET['myid'])

    print(ASSET.id)
    # text类型的8个
    ASSET.asset_name = request.POST['asset_name']
    ASSET.manage_ip = request.POST['manage_ip']
    ASSET.memo = request.POST['memo']
    ASSET.asset_no = request.POST['asset_no']
    ASSET.expire_day = request.POST['expire_day']
    ASSET.sn = request.POST['sn']
    # ASSET.model = request.POST['model']
    ASSET.purchase_day = request.POST['purchase_day']

    # 直接select标签的3个
    if request.POST['status']!="0":
        ASSET.status = request.POST['status']
    else:
        ASSET.status=None

    if request.POST['network_location']!="0":
        ASSET.network_location = request.POST['network_location']
    else:
        ASSET.network_location=None

    ASSET.asset_type = request.POST['asset_type']

    # 外键的7个
    if request.POST['admin']!="0":
        ASSET.admin = User.objects.get(id=request.POST['admin'])
    else:
        ASSET.admin = None

    ASSET.model=Device_model.objects.get(id=request.POST['model'])

    # ASSET.vendor = Vendor.objects.get(id=request.POST['vendor'])
    if request.POST['organization']!='0':
        ASSET.organization = Organization.objects.get(id=request.POST['organization'])
    else:
        ASSET.organization=None
    if request.POST['idc']!="0":
        ASSET.idc = Idc.objects.get(id=request.POST['idc'])
    else:
        ASSET.idc = None
    if request.POST['cabinet'] !="0":
        ASSET.cabinet = Cabinet.objects.get(id=request.POST['cabinet'])
    else:
        ASSET.cabinet=None
    if request.POST['contract']!="0":
        ASSET.contract = Contract.objects.get(id=request.POST['contract'])
    else:
        ASSET.contract=None
    if request.POST['supplier']!="0":
        ASSET.supplier = Supplier.objects.get(id=request.POST['supplier'])
    else:
        ASSET.supplier=None
    if request.POST['approved_by']!="0":
        ASSET.approved_by = User.objects.get(id=request.POST['approved_by'])
    else:
        ASSET.approved_by=None

    # 多对多1个，目前未考虑，暂时按照外键处理
    ASSET.save()
    # tag_list = request.POST.getlist('tag', '')
    # for t in tag_list:
    #     ASSET.tags.add(Tag.objects.get(id=t))
    # ASSET.save()

    CSSelected=CabinetSpace.objects.filter(asset=ASSET)
    for css in CSSelected:
        css.asset= None
        css.save()

    CapSpasId = request.POST.getlist('cabSpace')
    num=0
    hPlace=0
    if CapSpasId:
        print("有cabSpace哦")
        for cId in CapSpasId:
            num=num+1
            CABSPACE = CabinetSpace.objects.get(id=cId)
            if int(CABSPACE.cabinet_location)>hPlace:
                hPlace=int(CABSPACE.cabinet_location)
            CABSPACE.asset = ASSET
            CABSPACE.save()
        ASSET.height=num*22-2
        ASSET.cab_location=(ASSET.cabinet.cabinet_height-hPlace)*22+20
    else:
        ASSET.height=None
        ASSET.cab_location=None
    ASSET.save()
    print("!!!!!!!!!!!!!!!!!!!")
    print(ASSET.height)
    print(ASSET.cab_location)

    if ASSET.asset_type=="1" :
        if Server.objects.filter(asset=ASSET):
            SERVER=Server.objects.get(asset=ASSET)
        else:
            SERVER=Server()
            SERVER.asset=ASSET
        if request.POST['asset_subtype'] !='0':
            SERVER.sub_asset_type=request.POST['asset_subtype']
        else:
            SERVER.sub_asset_type=None
        if request.POST['hosted_on'] != '0':
            SERVER.hosted_on = Server.objects.get(id=request.POST['hosted_on'])
        else:
            SERVER.hosted_on=None
        SERVER.microcode=request.POST['microcode']
        if request.POST['os_type']!='0':
            SERVER.os_type = request.POST['os_type']
        else:
            SERVER.os_type=None
        SERVER.os_distribution = request.POST['os_distribution']
        SERVER.os_release = request.POST['os_release']
        SERVER.save()
    elif ASSET.asset_type=="2":
        if NetworkDevice.objects.filter(asset=ASSET):
            NETWORKDEVICE=NetworkDevice.objects.get(asset=ASSET)
        else:
            NETWORKDEVICE=NetworkDevice()
            NETWORKDEVICE.asset=ASSET
        if request.POST['asset_subtype']!='0':
            NETWORKDEVICE.sub_asset_type = request.POST['asset_subtype']
        else:
            NETWORKDEVICE.sub_asset_type=None
        NETWORKDEVICE.save()
    elif ASSET.asset_type == "3":
        if SecurityDevice.objects.filter(asset=ASSET):
            SECURITYDEVICE = SecurityDevice.objects.get(asset=ASSET)
        else:
            SECURITYDEVICE=SecurityDevice()
            SECURITYDEVICE.asset=ASSET
        if request.POST['asset_subtype']!='0':
            SECURITYDEVICE.sub_asset_type = request.POST['asset_subtype']
        else:
            SECURITYDEVICE.sub_asset_type=None
        SECURITYDEVICE.save()
    elif ASSET.asset_type=="4":
        if StorageDevice.objects.filter(asset=ASSET):
            STORAGEDEVICE = StorageDevice.objects.get(asset=ASSET)
        else:
            STORAGEDEVICE=StorageDevice()
            STORAGEDEVICE.asset=ASSET
        if request.POST['asset_subtype']!='0':
            STORAGEDEVICE.sub_asset_type = request.POST['asset_subtype']
        else:
            STORAGEDEVICE.sub_asset_type=None
        STORAGEDEVICE.save()

    Assets = Asset.objects.all()
    Organizations=Organization.objects.all()
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
    return render(request, 'cmdb/ServerManage/asset.html', context)

@login_required()
def orgManage(request):
    # 查询中线局对象
    zxj = Organization.objects.get(org_name="中线局")
    zxj_children = []

    # 查询分局局对象
    fenju_list = Organization.objects.filter(parent_org=zxj.id)

    # 生成各级组织名称
    for fenju in fenju_list:
        guanlichu_list = Organization.objects.filter(parent_org=fenju.id)
        # print(guanlichu_list)
        fenju_name = fenju.org_name
        list_tmp = []
        for guanlichu in guanlichu_list:
            xiandizhan_list = Organization.objects.filter(parent_org=guanlichu.id)
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
        'data': org_dic,
        'USERNAME': str(request.user),
        'Perm': Perm,
        'tab_number': "org",
    }

    return render(request, 'cmdb/basicData/orgManage.html', context)

@login_required()
def idcManage(request):
    """
    Organizations = Organization.objects.all()
    myIdc = Idc.objects.all()
    myOrg = Organization()
    myCabinet = Cabinet()
    cabFlag = 0
    print("^^^^^^^^^^^^^^^^^^^")
    print(type(myOrg))
    print(type(myCabinet))

    try:
        IDC = request.GET['IDC']
        myCabinet=Cabinet.objects.filter(idc=Idc.objects.get(id=IDC))
        cabFlag=1
    except:
        print("没有IDC参数!")

    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ORGS': Organizations,
        'myOrg': myOrg,
        'myIdcs': myIdc,
        'myCabs': myCabinet,
        'cabFlag':cabFlag,
        'tab_number': "idc",
    }
    return render(request, 'cmdb/basicData/idcManage.html', context)
"""
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    Idc_list = Idc.objects.all()
    peridc_asset_count = []
    for idc in Idc_list:
        servercount = len(idc.asset_set.filter(asset_type=1))
        netcount = len(idc.asset_set.filter(asset_type=2))
        securitycount = len(idc.asset_set.filter(asset_type=3))
        storgecount = len(idc.asset_set.filter(asset_type=4))

        asset_count = {"idc_name": idc.idc_name,
                       "data": {
                           "servercount": servercount,
                           "netcount": netcount,
                           "securitycount": securitycount,
                           "storgecount": storgecount,
                       }
                       }
        peridc_asset_count.append(asset_count)

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'IDC': Idc_list,
        'peridc_asset_count': peridc_asset_count,
    }
    return render(request, 'cmdb/basicData/idcManage.html', context)


'''
@login_required()
def idcManage(request):
    Organizations = Organization.objects.all()
    myOrg = Organization()
    myIdc = Idc.objects.all()
    myCabinet = Cabinet()
    cabFlag = 0
    zhongxianju=Organization.objects.get(org_name="中线局")
    Fenjus=Organization.objects.filter(parent_org=zhongxianju)

    try:
        IDC = request.GET['IDC']
        myCabinet=Cabinet.objects.filter(idc=Idc.objects.get(id=IDC))
        cabFlag=1
        print(myCabinet)
    except:
        print("没有IDC参数!")

    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'zhongxianju':zhongxianju,
        'Fenjus':Fenjus,
        'Guanlichus':None,
        'Xiandizhans':None,
        'USERNAME': str(request.user),
        'Perm': Perm,
        'ORGS': Organizations,
        'myOrg': myOrg,
        'myIdcs': myIdc,
        'myCabs': myCabinet,
        'cabFlag':cabFlag,
        'tab_number': "idc",
    }
    return render(request, 'cmdb/basicData/idcManage.html', context)
'''


@login_required()
def editCab(request):
    dCabinets = request.POST.getlist('delete_cabinets')
    if len(dCabinets):
        for i in dCabinets:
            Cabinet.objects.get(pk=i).delete()
    IDC=Idc.objects.get(id=request.GET['idcId'])
    Cabinets=Cabinet.objects.filter(idc=IDC)
    print(Cabinets)
    context={
        'IDC':IDC,
        'Cabinets':Cabinets,
    }
    return render (request, 'cmdb/basicData/editCab.html',context)
@login_required()
def addCabSubmit(request):
    IDC = Idc.objects.get(id=request.POST['idcId'])
    CAB=Cabinet()
    CAB.idc=IDC
    CAB.cabinet_name=request.POST['name']
    CAB.cabinet_desc=request.POST['desc']
    CAB.cabinet_height=request.POST['height']
    CAB.save()
    Cabinets = Cabinet.objects.filter(idc=IDC)
    for i in range(1,int(request.POST['height'])+1):
        CABSPACE=CabinetSpace()
        CABSPACE.cabinet=CAB
        CABSPACE.cabinet_location=str(i)
        CABSPACE.save()
        print(CABSPACE)
    context = {
        'IDC': IDC,
        'Cabinets': Cabinets,
    }
    return render(request, 'cmdb/basicData/editCab.html', context)
@login_required()
def addIdc(request):
    Organizations=Organization.objects.all()
    successFlag=0
    context={
        'successFlag':successFlag,
        'Organizations':Organizations,
    }
    return render (request,'cmdb/basicData/addIdc.html',context)
@login_required()
def idcSubmit(request):
    print(request.POST)
    IDC=Idc()
    IDC.idc_name=request.POST['name']
    IDC.idc_address=request.POST['address']
    IDC.organization=Organization.objects.get(id=request.POST['organization'])
    IDC.idc_memo=request.POST['memo']
    IDC.save()
    print(IDC)
    successFlag=1
    Organizations = Organization.objects.all()
    context = {
        'successFlag':successFlag,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/basicData/addIdc.html', context)
@login_required()
def editIdc (request):
    IDC = Idc.objects.get(id=request.GET['idcId'])
    Organizations = Organization.objects.all()
    successFlag = 0
    context = {
        'IDC':IDC,
        'successFlag': successFlag,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/basicData/editIdc.html', context)
@login_required()
def submitIdcEdit(request):
    print(request.POST)
    IDC = Idc.objects.get(id=request.GET['idcId'])
    IDC.idc_name=request.POST['name']
    IDC.idc_address=request.POST['address']
    IDC.organization=Organization.objects.get(id=request.POST['organization'])
    IDC.idc_memo=request.POST['memo']
    IDC.save()
    print(IDC)
    successFlag=1
    Organizations = Organization.objects.all()
    context = {
        'successFlag':successFlag,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/basicData/editIdc.html', context)
@login_required()
def deleteAIdc (request):
    IDC = Idc.objects.get(id=request.GET['idcId'])
    IDC.delete()
    successFlag = 2
    Organizations = Organization.objects.all()
    context = {
        'successFlag': successFlag,
        'Organizations': Organizations,
    }
    return render(request, 'cmdb/basicData/editIdc.html', context)

@login_required()
def cabDetail(request):
    IDC=Idc.objects.get(id=request.GET['idcId'])
    CABS=Cabinet.objects.filter(idc=IDC)
    assets=Asset.objects.filter(idc=IDC)
    ASSETS=set()
    for a in assets:
        if a.cab_location:
            ASSETS.add(a)

    context={
        'IDC':IDC,
        'CABS':CABS,
        'ASSETS':ASSETS,
    }
    return render (request,'cmdb/basicData/cabDetail.html',context)


@login_required()
def userManage(request):
    dadmin = request.POST.getlist('delete_admin')
    if len(dadmin):
        for i in dadmin:
            User.objects.get(pk=i).delete()
    admin=User.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Perm': Perm,
        'tab_number': "user",
    }
    return render(request,'cmdb/basicData/userManage.html',context)

@login_required()
def addUserSubmit(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    if str(request.POST['perm']) != '0':
        user.is_superuser = True
    user.save()
    admin = User.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'admin': admin,
        'USERNAME': str(request.user),
        'Perm': Perm,
    }
    return render(request,'cmdb/basicData/userManage.html',context)

@login_required()
def contractManage(request):
    dcontract = request.POST.getlist('delete_contract')
    if len(dcontract):
        for i in dcontract:
            Contract.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    contract = Contract.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'contract': contract,
        'USERNAME': str(request.user),
        'Perm': Perm,
        'tab_number': "contract",
    }
    return render(request,'cmdb/basicData/contractManage.html',context)

@login_required()
def addContractSubmit(request):
    o = Contract()
    o.contract_number = request.POST['number']
    o.contract_name = request.POST['name']
    o.contract_content = request.POST['content']
    o.contract_memo = request.POST['memo']
    o.save()
    contract = Contract.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'contract': contract,
        'USERNAME': str(request.user),
        'Perm': Perm,
    }
    return render(request,'cmdb/basicData/contractManage.html',context)


@login_required()
def editOrg(request):
    # 判断是否有删除请求，有则删除厂商
    dorg = request.POST.getlist('delete_org')
    print(dorg)
    if len(dorg):
        for i in dorg:
           Organization.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    org = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'org': org
    }
    return render(request, 'cmdb/basicData/editOrg.html',context)

@login_required()
def addOrgSubmit(request):
    o = Organization()
    o.org_name=request.POST['name']
    o.org_address = request.POST['address']
    o.org_memo=request.POST['memo']
    parent_org=Organization.objects.get(id=request.POST['parent_org'])
    o.parent_org=parent_org
    o.save()
    org = Organization.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'org': org,
    }

    return render(request, 'cmdb/basicData/editOrg.html', context)

def supplierManage(request):
 # 判断是否有删除请求，有则删除厂商
    dsupplier = request.POST.getlist('delete_supplier')
    if len(dsupplier):
        for i in dsupplier:
            Supplier.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier,
        'tab_number': "supplier",
    }
    return render(request, 'cmdb/basicData/supplierManage.html',context)

@login_required()
def addSupplierSubmitM(request):
    o = Supplier()
    o.supplier_name = request.POST['name']
    o.supplier_contacts = request.POST['contact']
    o.supplier_phone = request.POST['phone']
    o.supplier_memo = request.POST['memo']
    o.save()
    supplier = Supplier.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'supplier': supplier
    }

    return render(request, 'cmdb/basicData/supplierManage.html', context)

def vendorManage(request):
    # 判断是否有删除请求，有则删除厂商
    dvendor = request.POST.getlist('delete_vendor')
    print(dvendor)
    if len(dvendor):
        for i in dvendor:
           Vendor.objects.get(pk=i).delete()

    # 查询现有所有厂商对象并传给前段页面
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor,
        'tab_number': "vendor",
    }
    return render(request, 'cmdb/basicData/vendorManage.html',context)

@login_required()
def addVendorSubmitM(request):
    o = Vendor()
    o.vendor_name=request.POST['name']
    o.vendor_phone=request.POST['phone']
    o.vendor_memo=request.POST['memo']
    o.save()
    vendor = Vendor.objects.all()
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'vendor': vendor
    }

    return render(request, 'cmdb/basicData/vendorManage.html', context)


@login_required()
def assetMap(request):
    if request.user.is_superuser:
        Perm = 1
    else:
        Perm = 0
    Idc_list = Idc.objects.all()
    peridc_asset_count = []
    for idc in Idc_list:
        servercount= len(idc.asset_set.filter(asset_type=1))
        netcount= len(idc.asset_set.filter(asset_type=2))
        securitycount= len(idc.asset_set.filter(asset_type=3))
        storgecount= len(idc.asset_set.filter(asset_type=4))

        asset_count={"idc_name":idc.idc_name,
                     "data": {
                            "servercount": servercount,
                            "netcount": netcount,
                            "securitycount": securitycount,
                            "storgecount": storgecount,
                            }
                      }
        peridc_asset_count.append(asset_count)

    context = {
        'USERNAME': str(request.user),
        'Perm': Perm,
        'IDC': Idc_list,
        'peridc_asset_count':peridc_asset_count,
    }
    return render(request, 'cmdb/assetMap.html', context)


#根据设备类型返回设备子类型
def subtype(request, id):
     asset_type = int(id)
     subtype_list = []
     if asset_type == 1:
         subtype_list = [
             {"id": 1, "type": "PC服务器"},
             {"id": 2, "type": "小型机"},
             {"id": 3, "type": "刀片机"},
             {"id": 4, "type": "虚拟机"},
             {"id": 5, "type": "容器"},
         ]

     if asset_type == 2:
         subtype_list = [
             {"id": 1, "type": "路由器"},
             {"id": 2, "type": "交换机"},
             {"id": 3, "type": "工业交换机"},
             {"id": 4, "type": "无线控制器"},
             {"id": 5, "type": "无线AP"},
         ]

     if asset_type == 3:
         subtype_list = [
             {"id": 1, "type": "防火墙"},
             {"id": 2, "type": "入侵检测设备"},
             {"id": 3, "type": "入侵防御设备"},
             {"id": 4, "type": "综合安全网关"},
             {"id": 5, "type": "数据库审计系统"},
             {"id": 6, "type": "运维审计系统"},
             {"id": 7, "type": "防病毒网关"},
             {"id": 8, "type": "WAF防火墙"},
             {"id": 9, "type": "安全配置核查"},
             {"id": 10, "type": "网络准入系统"},
             {"id": 11, "type": "网闸设备"},
             {"id": 12, "type": "VPN设备"},
         ]
     if asset_type == 4:
         subtype_list = [
             {"id": 1, "type": "磁盘阵列"},
             {"id": 2, "type": "网络存储器"},
             {"id": 3, "type": "光纤交换机"},
             {"id": 4, "type": "磁带库"},
             {"id": 5, "type": "磁带机"},
         ]

     return  JsonResponse({"data":subtype_list})


#根据厂商返回设备型号
def devicemodel(request, vendor):
    vendor_id = vendor
    model_list = []
    models = Device_model.objects.filter(vendor_id=vendor_id)
    for m in models:
        temp = {"id":m.id,"model":m.models}
        model_list.append(temp)

    return JsonResponse({"data": model_list})







